#!/usr/bin/env python3
"""Merge 4K candidates that passed both discovery and a separate recheck.

Does not perform network tests; run audit_streams.py to refresh reports first.
Keeps all existing entries and only adds URLs measured at >=3840x2160.
"""
import hashlib
import json
import re
from pathlib import Path

from refresh_playlist import merge, name_of, normalized, now, parse_m3u

ROOT = Path(__file__).resolve().parents[1]


def read_results(name):
    report = json.loads((ROOT / 'reports' / name).read_text())
    if not report.get('complete') or len(report['results']) != report.get('source_count'):
        raise ValueError(f'测试报告尚未完成: {name}')
    return report['results']


def is_4k(result):
    return (result['status'] == 'passed'
            and (result.get('width') or 0) >= 3840
            and (result.get('height') or 0) >= 2160)


def main():
    discovered = {r['url']: r for name in ('4k-multicast-audit.json', '4k-internet-audit.json')
                  for r in read_results(name) if is_4k(r)}
    checked = [r for name in ('4k-local-recheck.json', '4k-web-recheck.json')
               for r in read_results(name) if is_4k(r) and r['url'] in discovered]
    target = ROOT / 'shtelconiptv.m3u'
    _, entries = parse_m3u(target.read_text())
    # Preserve the original selection so repeat merges retain channel/backup labels.
    selection_path = ROOT / 'reports/4k-selected.json'
    old_selection = json.loads(selection_path.read_text()) if selection_path.exists() else {}
    base_names = old_selection.get('base_4k_channels') or [name_of(e) for e in entries
                  if 'group-title="4K超高清"' in e['info']]
    known_channels = {normalized(name) for name in base_names}
    selected = []
    for result in checked:
        item = dict(result)
        channel = item['channel']
        # The actual picture is "美丽河北" landscape TV, not 河北卫视.
        if item['url'] == 'https://event.pull.hebtv.com/live/live101.m3u8':
            channel = '美丽河北4K'
        backup = normalized(channel) in known_channels
        source = '组播' if '/udp/' in item['url'] else '公网'
        item.update(channel=channel, source_label=source + ('备用' if backup else ''),
                    group='4K超高清', role='backup' if backup else 'new_channel',
                    first_checked_at=discovered[item['url']]['checked_at'])
        selected.append(item)
    selected.sort(key=lambda r: r['role'] == 'backup')
    added, groups = merge(selected, target)
    data = dict(merged_at=now(), source_reports=['4k-multicast-audit.json', '4k-internet-audit.json',
                '4k-local-recheck.json', '4k-web-recheck.json'],
                base_4k_channels=base_names, distinct_new_channels=[r['channel'] for r in selected
                if r['role'] == 'new_channel'], selected=selected,
                total_4k_entries=groups.get('4K超高清', 0),
                playlist_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    selection_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(new_entries_this_run=len(added),
          distinct_new_channels=data['distinct_new_channels'], groups=groups), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
