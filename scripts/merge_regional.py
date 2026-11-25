#!/usr/bin/env python3
"""Merge regional candidates after two completed audits and visual review."""
import hashlib
import json
from pathlib import Path

from refresh_playlist import merge, now

ROOT = Path(__file__).resolve().parents[1]


def completed(name):
    data = json.loads((ROOT / 'reports' / name).read_text())
    if not data.get('complete') or data['source_count'] != len(data['results']):
        raise ValueError('测试报告尚未完成: ' + name)
    return data['results']


def main():
    first = {r['url'] for r in completed('regional-discovery.json')
             if r['status'] == 'passed'}
    selected = [r for r in completed('regional-recheck.json')
                if r['status'] == 'passed' and r['url'] in first
                and r.get('visual_verified')]
    target = ROOT / 'shtelconiptv.m3u'
    added, groups = merge(selected, target)
    report = dict(merged_at=now(), selected=selected, playlist_groups=dict(groups),
                  playlist_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (ROOT / 'reports/regional-selected.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(added=len(added), selected=len(selected), groups=groups),
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
