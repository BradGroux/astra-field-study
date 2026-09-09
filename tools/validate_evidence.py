#!/usr/bin/env python3
"""Validate the separate observational evidence format locally; no uploads."""
import argparse
import json
from pathlib import Path
import sys

from evidence_schema import (SCHEMA, TOKEN_FIELDS, USAGE_FIELDS, PARTITION_FIELDS,
                             EPISODE_FIELDS, OUTCOMES, EVENT_FIELDS, CATEGORIES,
                             CATEGORY_FIELDS)
from validate import ValidationError, check, load, require

ADDITIVE_USAGE = tuple(k for k in USAGE_FIELDS if k not in ('tasks', 'completed_interval_union_ms'))
CODING_COUNTS = PARTITION_FIELDS + EPISODE_FIELDS


def unique(rows, fields):
    keys = [tuple(row[k] for k in fields) for row in rows]
    require(len(keys) == len(set(keys)), 'Repeated grouping key.')


def usage_row(row):
    t = row['tokens']
    require(t['input_tokens'] + t['output_tokens'] == t['total_tokens'], 'Token accounting mismatch.')
    require(t['input_tokens'] - t['cached_input_tokens'] == t['uncached_input_tokens'], 'Input accounting mismatch.')
    require(t['reasoning_output_tokens'] <= t['output_tokens'], 'Output accounting mismatch.')
    require(row['turns'] == row['completed_turns'] + row['incomplete_turns'], 'Turn accounting mismatch.')
    require(row['completed_interval_union_ms'] <= row['sum_completed_turn_ms'], 'Duration accounting mismatch.')


def usage_partition(rows, summary):
    for k in ADDITIVE_USAGE:
        require(sum(r[k] for r in rows) == summary[k], 'Usage partition mismatch.')
    for k in TOKEN_FIELDS:
        require(sum(r['tokens'][k] for r in rows) == summary['tokens'][k], 'Token partition mismatch.')
    for k in ('tasks', 'completed_interval_union_ms'):
        values = [r[k] for r in rows]
        require(max(values, default=0) <= summary[k] <= sum(values), 'Non-additive count bounds mismatch.')


def coding_row(row, episodes=True):
    require(row['eligible'] == sum(row[k] for k in ('D_only', 'C_only', 'both', 'routine', 'ambiguous')),
            'Exclusive partition mismatch.')
    require(row['dissatisfaction_units'] == row['D_only'] + row['both'], 'Dissatisfaction accounting mismatch.')
    require(row['corrective_units'] == row['C_only'] + row['both'], 'Correction accounting mismatch.')
    require(row['union'] == row['D_only'] + row['C_only'] + row['both'], 'Overlap accounting mismatch.')
    if episodes:
        require(sum(row['outcomes'].values()) == row['correction_episodes'], 'Episode outcomes mismatch.')
        require(row['repeated_correction_episodes'] <= row['correction_episodes'], 'Repeated episode count mismatch.')
        require(row['process_correction_episodes'] <= row['correction_episodes'], 'Process episode count mismatch.')
        require(row['process_correction_units'] <= row['corrective_units'], 'Process unit count mismatch.')
        # Episodes use first-correction onset. A day's episode may have later corrections
        # elsewhere; do not impose per-day repeated-membership bounds here.


def coding_partition(rows, summary, episodes=True):
    for k in CODING_COUNTS if episodes else PARTITION_FIELDS:
        require(sum(r[k] for r in rows) == summary[k], 'Coded partition mismatch.')
    if episodes:
        for k in OUTCOMES:
            require(sum(r['outcomes'][k] for r in rows) == summary['outcomes'][k], 'Outcome partition mismatch.')


def validate_evidence(data, ready=False):
    check(data, SCHEMA)
    if ready:
        require(all(data['consent'].values()), 'Explicit public release and MIT consent required.')
    u, c, r = data['usage'], data['coded_observations'], data['repository_activity']
    usage_row(u['summary'])
    for name, dimensions in [('by_day', ('day',)), ('by_project', ('project',)),
                             ('by_observer', ('observer',)),
                             ('by_day_project_observer', ('day', 'project', 'observer'))]:
        unique(u[name], dimensions)
        for row in u[name]:
            usage_row(row)
            if 'day' in row:
                require(row['day'] <= data['study_days'], 'Day outside window.')
        usage_partition(u[name], u['summary'])
    require({x['day'] for x in u['by_day']} == set(range(1, data['study_days'] + 1)), 'Incomplete daily coverage.')
    for name, field in [('by_day', 'day'), ('by_project', 'project'), ('by_observer', 'observer')]:
        require({x[field] for x in u['by_day_project_observer']} <= {x[field] for x in u[name]},
                'Unknown usage group.')
        for total in u[name]:
            usage_partition([x for x in u['by_day_project_observer'] if x[field] == total[field]], total)
    coding_row(c['summary'])
    require(c['summary']['correction_episodes'] <= c['summary']['corrective_units'], 'Episodes exceed corrective units.')
    require(c['summary']['correction_episodes'] + c['summary']['repeated_correction_episodes'] <= c['summary']['corrective_units'],
            'Repeated episodes require distinct corrective units.')
    for name, dimensions in [('by_day', ('day',)), ('by_project', ('project',)),
                             ('by_day_project', ('day', 'project')), ('by_surface', ('surface',))]:
        unique(c[name], dimensions)
        for row in c[name]:
            coding_row(row, name != 'by_surface')
            if 'day' in row:
                require(row['day'] <= data['study_days'], 'Coded day outside window.')
        coding_partition(c[name], c['summary'], name != 'by_surface')
    require({x['day'] for x in c['by_day']} == set(range(1, data['study_days'] + 1)), 'Incomplete coded daily coverage.')
    for name, field in [('by_day', 'day'), ('by_project', 'project')]:
        require({x[field] for x in c['by_day_project']} <= {x[field] for x in c[name]}, 'Unknown coded group.')
        for total in c[name]:
            coding_partition([x for x in c['by_day_project'] if x[field] == total[field]], total)
    projects = {x['project'] for x in u['by_project']}
    require({x['project'] for x in c['by_project']} <= projects, 'Unknown coded project.')
    unique(r['by_project'], ('project',))
    require({x['project'] for x in r['by_project']} <= projects, 'Unknown repository project.')
    require(len(r['by_project']) == r['identifiable_repositories'], 'Repository coverage mismatch.')
    require(len(projects) == r['identifiable_repositories'] + r['unresolved_projects'], 'Unresolved project count mismatch.')
    for k in EVENT_FIELDS:
        require(sum(x['events'][k] for x in r['by_project']) == r['events'][k], 'Repository event partition mismatch.')
    for events in [r['events']] + [x['events'] for x in r['by_project']]:
        require(events['issue_active_in_window'] == events['issue_active_state_open'] + events['issue_active_state_closed'],
                'Issue state mismatch.')
        require(events['pr_active_in_window'] == sum(events['pr_active_state_' + state] for state in ('open', 'closed', 'merged')),
                'PR state mismatch.')
        for kind in ('issue', 'pr'):
            for suffix in ('candidate_records', 'opened_in_window', 'distinct_with_close_event', 'distinct_reopened'):
                require(events[kind + '_' + suffix] <= events[kind + '_active_in_window'], 'Event population mismatch.')
        require(events['pr_merged_in_window'] <= events['pr_active_state_merged'], 'In-window merges exceed cutoff merged population.')
    n = r['net_changes']
    for summary_key, row_key in [('net_diff_additions', 'added'), ('net_diff_deletions', 'deleted'),
                                 ('net_changed_repository_qualified_paths', 'unique_paths')]:
        require(sum(x['net_diff'][row_key] for x in r['by_project']) == n[summary_key], 'Net diff partition mismatch.')
    require(n['net_line_delta'] == n['net_diff_additions'] - n['net_diff_deletions'], 'Net line delta mismatch.')
    require(sum(x['first_parent_commit_objects_in_window'] for x in r['by_project']) == n['first_parent_commit_objects_in_window'],
            'Commit object partition mismatch.')
    require(sum(x['net_files_complete'] for x in r['by_project']) == n['repositories_with_complete_net_diff'], 'Diff completeness mismatch.')
    require(sum(x['first_parent_commit_objects_in_window'] > 0 for x in r['by_project']) == n['repositories_with_default_branch_commit_activity'],
            'Commit coverage mismatch.')
    for row in r['by_project']:
        diff = row['net_diff']
        for field in CATEGORY_FIELDS:
            require(sum(diff['categories'][k][field] for k in CATEGORIES) == diff['file_touches' if field == 'touches' else field],
                    'Diff category partition mismatch.')
        require(diff['binary_touches'] <= diff['file_touches'], 'Binary path count mismatch.')
        require(diff['unique_paths'] <= diff['file_touches'], 'Unique path count mismatch.')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--ready', action='store_true')
    args = parser.parse_args()
    try:
        data = validate_evidence(load(args.file), args.ready)
    except (ValidationError, OSError, RecursionError, KeyError, TypeError):
        print('Rejected: observational evidence schema, accounting, consent or file check failed. No input content displayed.', file=sys.stderr)
        return 1
    print(json.dumps({'format_version': data['format_version'], 'synthetic': data['synthetic'],
                      'study_days': data['study_days'], 'responses': data['usage']['summary']['responses'],
                      'substantive_contributions': data['coded_observations']['summary']['eligible'],
                      'direct_ratings': data['direct_ratings']}, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
