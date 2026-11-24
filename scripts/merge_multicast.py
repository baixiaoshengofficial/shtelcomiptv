#!/usr/bin/env python3
"""Merge visually reviewed multicast channels after two completed audits.

Reads reports/multicast-reviewed.json, multicast-discovery.json and
multicast-recheck.json. It does not perform network discovery itself.
"""
import hashlib
import json
from pathlib import Path

from refresh_playlist import merge, now

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'


def verified_report(name):
    report = json.loads((REPORTS / name).read_text())
    if not report.get('complete') or report['source_count'] != len(report['results']):
        raise ValueError('测试报告尚未完成: ' + name)
    return {r['url']: r for r in report['results'] if r['status'] == 'passed'}


def main():
    first = verified_report('multicast-discovery.json')
    second = verified_report('multicast-recheck.json')
    reviewed = json.loads((REPORTS / 'multicast-reviewed.json').read_text())
    selected = []
    for decision in reviewed:
        url = decision['url']
        if not decision.get('visual_verified') or url not in first or url not in second:
            continue
        if second[url].get('media_type') != 'video':
            continue
        item = dict(second[url], **decision)
        item.setdefault('group', '上海')
        selected.append(item)
    target = ROOT / 'shtelconiptv.m3u'
    added, groups = merge(selected, target)
    # Display the current station name; keep the original EPG IDs/names/logos.
    text = target.read_text()
    text = text.replace(',欢笑剧场4K\n', ',多彩文体4K（原欢笑剧场）\n')
    text = text.replace(',欢笑剧场4K [组播备用]\n', ',多彩文体4K（原欢笑剧场） [组播备用]\n')
    target.write_text(text)
    result = dict(merged_at=now(), selected=selected, playlist_groups=dict(groups),
                  playlist_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                  station_name_reference='https://caigou.smg.cn/review/202604/0167257.html')
    (REPORTS / 'multicast-selected.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(added_this_run=len(added), selected=len(selected), groups=groups), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
