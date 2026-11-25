#!/usr/bin/env python3
"""Merge Asia streams that passed discovery, recheck and visual review.

This reads completed local reports and does not run new network tests.
"""
import hashlib
import json
from pathlib import Path

from refresh_playlist import merge, now

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'


def results(name):
    data = json.loads((REPORTS / name).read_text())
    if not data.get('complete') or data['source_count'] != len(data['results']):
        raise ValueError('测试报告尚未完成: ' + name)
    return data['results']


def main():
    first = {r['url'] for r in results('asia-discovery.json') if r['status'] == 'passed'}
    selected = [r for r in results('asia-recheck.json') if r['status'] == 'passed'
                and r['url'] in first and r.get('visual_verified')]
    target = ROOT / 'shtelconiptv.m3u'
    added, groups = merge(selected, target)
    report = dict(merged_at=now(), selected=selected, playlist_groups=dict(groups),
                  playlist_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (REPORTS / 'asia-selected.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(added_this_run=len(added), selected=len(selected), groups=groups), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
