#!/usr/bin/env python3
"""Validate captured EMOS sources, then merge passing sources into the M3U.

Requires Python 3.10+, curl, ffprobe and ffmpeg. No third-party Python packages.
Only sources with decoded live media are added; existing sources are preserved.
"""
import argparse
import concurrent.futures
import json
import re
import subprocess
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
GROUPS = ['4K超高清', '央视频道', '卫视频道', '上海本地', '体育竞技',
          '影视剧场', '少儿动漫', '财经理财', '纪实科教', '生活休闲',
          '教育课堂', '地方频道', '港澳频道', '国际频道', '广播电台', '其他频道']


def now():
    return datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')


def run(cmd, timeout=25):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def fetch(url, folder, name, seconds=15):
    target = folder / name
    p = run(['curl', '-sS', '-L', '--connect-timeout', '5', '--max-time', str(seconds),
             '--max-filesize', '33554432', '-o', str(target), '-w',
             '%{http_code}\n%{url_effective}', url], seconds + 3)
    info = p.stdout.splitlines()
    status = int(info[0]) if info and info[0].isdigit() else 0
    effective = info[1] if len(info) > 1 else url
    data = target.read_bytes() if target.exists() else b''
    if status >= 400 or not data or p.returncode not in (0, 28):
        detail = data[:350].decode('utf-8', errors='replace') if status >= 400 else p.stderr.strip()
        raise ValueError(f'HTTP {status}: {detail[:350]}')
    return data, effective, p.returncode == 0


def decode_sample(path):
    p = run(['ffprobe', '-v', 'error', '-show_entries',
             'stream=codec_type,codec_name,width,height,sample_rate,channels',
             '-of', 'json', str(path)], 20)
    if p.returncode:
        raise ValueError('ffprobe 无法识别媒体: ' + p.stderr[-300:])
    streams = json.loads(p.stdout).get('streams', [])
    video = next((s for s in streams if s.get('codec_type') == 'video'), None)
    audio = next((s for s in streams if s.get('codec_type') == 'audio'), None)
    if not video and not audio:
        raise ValueError('未识别到音视频轨道')
    p = run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-threads', '2',
             '-i', str(path), '-t', '3', '-map', '0:v:0?', '-map', '0:a:0?',
             '-progress', 'pipe:1', '-nostats', '-f', 'null', '-'], 30)
    progress = dict(re.findall(r'^(\w+)=(.*)$', p.stdout, re.M))
    duration = int(progress.get('out_time_us', '0')) / 1e6
    frames = int(progress.get('frame', '0').strip())
    if p.returncode or duration < 2 or (video and frames < 25):
        raise ValueError(f'解码失败或样本不足: {duration:.2f}s, {frames} 帧; {p.stderr[-250:]}')
    return dict(streams=streams, width=(video or {}).get('width'),
                height=(video or {}).get('height'), media_type='video' if video else 'audio',
                decoded_seconds=round(duration, 3), decoded_frames=frames)


def hls_sample(url, folder):
    data, effective, complete = fetch(url, folder, 'root', seconds=10)
    if not data.lstrip(b'\xef\xbb\xbf\r\n ').startswith(b'#EXTM3U'):
        # An extensionless source can return an MPEG transport stream directly.
        if data[:1] == b'G' and len(data) > 188 and data[188:189] == b'G':
            return folder / 'root', dict(transport='mpegts', resolved_url=effective)
        raise ValueError('返回内容不是 HLS 或 MPEG-TS 媒体')
    for depth in range(5):
        text = data.decode('utf-8-sig')
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        variants = []
        for i, line in enumerate(lines[:-1]):
            if line.startswith('#EXT-X-STREAM-INF:') and not lines[i+1].startswith('#'):
                bandwidth = re.search(r'BANDWIDTH=(\d+)', line)
                variants.append((int(bandwidth[1]) if bandwidth else 0, lines[i+1]))
        if not variants:
            break
        data, effective, complete = fetch(urljoin(effective, max(variants)[1]), folder, f'variant-{depth}')
    else:
        raise ValueError('HLS 嵌套层数过多')
    if not complete or '#EXTINF:' not in text:
        raise ValueError('不完整或无分片的 HLS 播放列表')
    if '#EXT-X-ENDLIST' in text:
        raise ValueError('点播或已经结束的 HLS，未作为直播添加')
    if any(line.startswith('#EXT-X-KEY:') and 'METHOD=NONE' not in line for line in lines):
        raise ValueError('加密 HLS 未完成解密测试，未添加')
    if '#EXT-X-BYTERANGE:' in text:
        raise ValueError('Byte-range HLS 未完成分片测试，未添加')
    chunks = [urljoin(effective, line) for line in lines if not line.startswith('#')]
    if not chunks:
        raise ValueError('HLS 没有媒体分片')
    selected = chunks[-3:-1] if len(chunks) >= 3 else chunks[:2]
    sample = bytearray()
    init = re.search(r'#EXT-X-MAP:.*?URI="([^"]+)"', text)
    if init:
        part, _, ok = fetch(urljoin(effective, init[1]), folder, 'init')
        if not ok:
            raise ValueError('初始化分片下载不完整')
        sample.extend(part)
    for i, chunk in enumerate(selected):
        part, _, ok = fetch(chunk, folder, f'segment-{i}')
        if not ok:
            raise ValueError('媒体分片下载不完整')
        sample.extend(part)
    path = folder / ('sample.mp4' if init else 'sample.ts')
    path.write_bytes(sample)
    return path, dict(transport='hls', resolved_url=effective,
                      segments_downloaded=len(selected), sample_bytes=len(sample))


def validate(source):
    result = dict(source, checked_at=now(), status='failed')
    url = source['url']
    if '://' not in url:
        return dict(result, status='platform_only', reason='平台内部频道代号，不是独立播放地址')
    if source['channel'] in ('奇幻西游:新世界', '情书.1995'):
        return dict(result, status='excluded_vod', reason='点播影片，不属于直播频道')
    try:
        with tempfile.TemporaryDirectory(prefix='iptv-check-') as tmp:
            folder = Path(tmp)
            if url.endswith('.txt'):
                data, _, _ = fetch(url, folder, 'subscription')
                return dict(result, status='excluded_subscription',
                            reason='订阅内容为升级/打赏/安装教程 MP4，不含直播频道',
                            content_preview=data.decode('utf-8-sig', errors='replace')[:1200])
            if url.startswith('rtsp://'):
                p = run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-rw_timeout',
                         '8000000', '-rtsp_transport', 'tcp', '-i', url,
                         '-t', '4', '-c', 'copy', '-y', str(folder / 'rtsp.ts')], 16)
                if p.returncode:
                    raise ValueError('RTSP 连接失败: ' + p.stderr[-300:])
                sample, details = folder / 'rtsp.ts', dict(transport='rtsp')
            else:
                sample, details = hls_sample(url, folder)
            result.update(details)
            result.update(decode_sample(sample))
            result['status'] = 'passed'
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        result['reason'] = str(error)[:600]
    return result


def category(name, old_group='', height=None, audio=False):
    if audio or name.startswith('RTHK'):
        return '广播电台'
    if (height or 0) >= 2160 or re.search(r'4K|UHD|超高清', name, re.I):
        return '4K超高清'
    if name.startswith('CCTV'):
        return '央视频道'
    if name.startswith(('CGTN', 'CGNTV', 'BreadTV')):
        return '国际频道'
    if name in ('翡翠台', '明珠台', 'TVB Plus'):
        return '港澳频道'
    if '卫视' in name:
        return '卫视频道'
    for words, group in [
        ('体育|足球|台球|高尔夫|网球|垂钓', '体育竞技'),
        ('CHC|电影|影视|剧场', '影视剧场'),
        ('少儿|卡通|动漫|炫动', '少儿动漫'),
        ('财经|理财|财富', '财经理财'),
        ('纪实|地理|科技', '纪实科教'),
        ('教育|学堂', '教育课堂'),
        ('时尚|乐游|茶频道|风云音乐|文化精品|游戏风云', '生活休闲'),
    ]:
        if re.search(words, name):
            return group
    if old_group in ('上海', '上海本地'):
        return '上海本地'
    if old_group in ('地方', '地方频道') or name.startswith('广东珠江'):
        return '地方频道'
    return '其他频道'


def parse_m3u(text):
    header = text.splitlines()[0]
    entries, pending = [], None
    for raw in text.splitlines()[1:]:
        line = raw.strip()
        if not line:
            continue
        if line.startswith('#EXTINF:'):
            if pending:
                raise ValueError('EXTINF 缺少播放地址')
            pending = dict(info=line, options=[])
        elif pending and line.startswith('#'):
            pending['options'].append(line)
        elif pending:
            pending['url'] = line
            entries.append(pending)
            pending = None
        else:
            raise ValueError('播放列表存在未配对的行: ' + line)
    if pending:
        raise ValueError('文件末尾 EXTINF 缺少播放地址')
    return header, entries


def name_of(entry):
    return entry['info'].split(',', 1)[1]


def normalized(name):
    return re.sub(r'[\s-]|HD|4K|超高清', '', name, flags=re.I).upper()


def merge(results, target):
    header, entries = parse_m3u(target.read_text())
    original_urls = Counter(e['url'] for e in entries)
    for e in entries:
        old = re.search(r'group-title="([^"]*)"', e['info'])
        group = category(name_of(e), old[1] if old else '')
        e['info'] = re.sub(r'group-title="[^"]*"', f'group-title="{group}"', e['info'])
    seen, added = set(original_urls), []
    for r in results:
        if r['status'] != 'passed' or r['url'] in seen:
            continue
        group = category(r['channel'], r['group'], r.get('height'), r.get('media_type') == 'audio')
        channel_name = re.sub(r'["\r\n]', '', r['channel'])
        template = next((e for e in entries if normalized(name_of(e)) == normalized(channel_name)), None)
        # Reuse EPG identity; use measured resolution to label the added source.
        attributes = ' '.join(re.findall(r'tvg-(?:id|name|logo)="[^"]*"', template['info'])) if template else f'tvg-name="{channel_name}"'
        quality = '4K' if (r.get('height') or 0) >= 2160 else ('HD' if (r.get('height') or 0) >= 720 else '')
        display = f'{channel_name}{quality} [EMOS]'
        if any(name_of(e) == display for e in entries):
            display = f'{channel_name}{quality} [EMOS {sum(1 for a in added if a["channel"] == channel_name)+1}]'
        entries.append(dict(info=f'#EXTINF:-1 {attributes} group-title="{group}",{display}', options=[], url=r['url']))
        seen.add(r['url'])
        added.append(dict(channel=channel_name, name=display, group=group, url=r['url']))
    entries.sort(key=lambda e: GROUPS.index(re.search(r'group-title="([^"]*)"', e['info'])[1]))
    output = header + '\n\n' + '\n\n'.join('\n'.join([e['info'], *e['options'], e['url']]) for e in entries) + '\n'
    _, checked = parse_m3u(output)
    assert original_urls <= Counter(e['url'] for e in checked), '原有播放地址不得丢失'
    assert len(checked) == len(entries)
    assert all(re.search(r'group-title="4K超高清"', e['info']) for e in checked if re.search('4K|UHD|超高清', name_of(e), re.I))
    target.write_text(output)
    return added, Counter(re.search(r'group-title="([^"]*)"', e['info'])[1] for e in checked)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--reuse-report', action='store_true', help='只使用已有测试报告重新分组/合并，不重新联网')
    args = parser.parse_args()
    report_path = ROOT / 'reports/validation.json'
    if args.reuse_report:
        report = json.loads(report_path.read_text())
    else:
        captured = json.loads((ROOT / 'reports/emos-sources.json').read_text())
        sources, seen = [], set()
        for c in captured['channels']:
            for s in c['sources']:
                if s['url'] not in seen:
                    sources.append(dict(channel=c['channel'], group=c['group'], **s))
                    seen.add(s['url'])
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            for r in pool.map(validate, sources):
                results.append(r)
                print(f'{r["status"]:22} {r["channel"]} {r["url"]}', flush=True)
        report = dict(tested_at=now(), source=captured['source'],
                      method='下载真实 HLS 分片/RTSP 样本；ffprobe 识别轨道；ffmpeg 解码至少 2 秒，视频至少 25 帧；原始直播 URL 原样合并',
                      captured_channels=len(captured['channels']),
                      captured_records=sum(len(c['sources']) for c in captured['channels']),
                      results=results)
    added, groups = merge(report['results'], ROOT / 'shtelconiptv.m3u')
    previously_added = report.get('newly_added', [])
    known_added = {a['url'] for a in previously_added}
    report.update(merged_at=now(), status_counts=dict(Counter(r['status'] for r in report['results'])),
                  newly_added=previously_added + [a for a in added if a['url'] not in known_added],
                  playlist_groups=dict(groups))
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(status_counts=report['status_counts'], newly_added=len(added), groups=groups), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
