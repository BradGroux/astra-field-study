#!/usr/bin/env python3
"""Derive only allowlisted explorer rows from validated public evidence."""
import argparse
import json
from pathlib import Path
import sys

from validate import load, ValidationError
from validate_evidence import validate_evidence
from evidence_schema import PARTITION_FIELDS

METRICS = ('responses', 'input_tokens', 'cached_input_tokens',
           'uncached_input_tokens', 'output_tokens', 'total_tokens')
DEFINITIONS = {
    'usage': 'Recorded response/token counters, not unique text, spend or productivity. Cached input is included in input; reasoning is included in output.',
    'coding': 'Protocol 1.1 substantive contributions. C = corrective steering; D = explicit dissatisfaction. Overlap is counted once in the union. Not a failure rate or CSAT.',
    'repository': 'All-author repository activity over the full study window. No daily outcome allocation or proven Astra authorship.',
    'privacy': 'Generic project labels, relative days, no public joins to named source projects. De-identification does not guarantee anonymity.',
}


def reader_data(evidence):
    validate_evidence(evidence)
    u = evidence['usage']
    coding = {(x['day'], x['project']): x for x in evidence['coded_observations']['by_day_project']}
    cells = {}
    for x in u['by_day_project_observer']:
        row = cells.setdefault((x['day'], x['project']), {k: 0 for k in METRICS})
        for k in METRICS:
            row[k] += x[k] if k == 'responses' else x['tokens'][k]
    rows = []
    for day in range(1, evidence['study_days'] + 1):
        for project in sorted(x['project'] for x in u['by_project']):
            row = {'day': day, 'project': project, **cells.get((day, project), {k: 0 for k in METRICS})}
            row.update({k: coding.get((day, project), {}).get(k, 0) for k in PARTITION_FIELDS})
            rows.append(row)
    repository = []
    for x in evidence['repository_activity']['by_project']:
        repository.append({'project': x['project'], 'issues': x['events']['issue_active_in_window'],
                           'merged': x['events']['pr_merged_in_window'], 'paths': x['net_diff']['unique_paths'],
                           'added': x['net_diff']['added'], 'deleted': x['net_diff']['deleted']})
    return {'format': 'observational_evidence_reader', 'format_version': '1.0',
            'synthetic': evidence['synthetic'], 'study_days': evidence['study_days'],
            'rows': rows, 'repository': repository, 'definitions': DEFINITIONS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--replace', action='store_true', help='Replace an existing derived reader file.')
    args = parser.parse_args()
    try:
        data = reader_data(load(args.evidence))
        with args.out.open('w' if args.replace else 'x') as stream:
            json.dump(data, stream, indent=2)
            stream.write('\n')
    except (ValidationError, OSError, RecursionError, KeyError, TypeError):
        print('Rejected: invalid evidence or unavailable output. No input content displayed.', file=sys.stderr)
        return 1
    print('Derived allowlisted reader data. No network access or upload.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
