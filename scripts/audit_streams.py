#!/usr/bin/env python3
"""Audit explicitly listed IPTV URLs, including udpxy MPEG-TS streams.

Input: JSON array of objects with channel and url. Output: timestamped results.
Multicast proxy tests should run with --workers 1 to avoid overloading udpxy.
"""
import argparse
import concurrent.futures
import json
import subprocess
import tempfile
from pathlib import Path

from refresh_playlist import decode_sample, hls_sample, now, run


def check(item, sample_seconds=5, keep_samples=None):
    result = dict(item, checked_at=now(), status='failed')
    try:
        with tempfile.TemporaryDirectory(prefix='iptv-audit-') as tmp:
            folder = Path(tmp)
            if '/udp/' in item['url'] or '/rtp/' in item['url']:
                sample = folder / 'sample.ts'
                p = run(['curl', '--noproxy', '*', '-sS', '--connect-timeout', '3',
                         '--max-time', str(sample_seconds), '--max-filesize', '50331648',
                         '-o', str(sample), '-w', '%{http_code}', item['url']], sample_seconds + 3)
                result.update(http_status=p.stdout, sample_bytes=sample.stat().st_size if sample.exists() else 0)
                # A live MPEG-TS response has no EOF: curl's time limit is expected.
                if p.stdout != '200' or not sample.exists() or sample.stat().st_size < 18800:
                    raise ValueError(f'无有效媒体数据: HTTP {p.stdout}, {result["sample_bytes"]} bytes; {p.stderr[-200:]}')
                if p.returncode not in (0, 28):
                    raise ValueError(f'下载异常: curl {p.returncode}; {p.stderr[-200:]}')
                result['transport'] = 'udpxy'
            else:
                sample, details = hls_sample(item['url'], folder)
                result.update(details)
            result.update(decode_sample(sample))
            result['status'] = 'passed'
            if keep_samples and result.get('media_type') == 'video':
                destination = Path(keep_samples)
                destination.mkdir(parents=True, exist_ok=True)
                import hashlib
                key = hashlib.sha256(item['url'].encode()).hexdigest()[:16]
                path = destination / (key + '.jpg')
                p = run(['ffmpeg', '-v', 'error', '-threads', '2', '-ss', '1',
                         '-i', str(sample), '-frames:v', '1', '-vf', 'scale=640:-1',
                         '-y', str(path)], 25)
                if p.returncode == 0:
                    result['preview'] = str(path)
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        result['reason'] = str(error)[:600]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--sample-seconds', type=int, default=5)
    parser.add_argument('--keep-samples')
    args = parser.parse_args()
    sources = json.loads(Path(args.input).read_text())
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check, item, args.sample_seconds, args.keep_samples): item for item in sources}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(f'{len(results)}/{len(sources)} {result["status"]} {result["channel"]} '
                  f'{result.get("width", "")}x{result.get("height", "")} {result["url"]}', flush=True)
            Path(args.output).write_text(json.dumps(dict(tested_at=now(), source_count=len(sources),
                complete=len(results) == len(sources), results=results), ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
