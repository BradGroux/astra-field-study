#!/usr/bin/env python3
"""Local allowlist, accounting and consent validation. No network access."""
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {'1.0': ROOT/'schema/submission-v1.schema.json', '1.1': ROOT/'schema/submission-v1.1.schema.json'}
MAX_BYTES = 1_000_000
class ValidationError(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise ValidationError(message)

def check(value, spec):
    if 'anyOf' in spec:
        for option in spec['anyOf']:
            try:
                check(value, option)
                return
            except ValidationError:
                pass
        raise ValidationError('Invalid optional value.')
    kind = spec.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool, 'null': type(None)}
    require(type(value) is types[kind], 'Invalid value type.')
    if 'enum' in spec:
        require(value in spec['enum'], 'Value outside allowed vocabulary.')
    if kind == 'object':
        require(set(spec['required']) <= set(value) <= set(spec['properties']), 'Unexpected or missing fields; export rejected.')
        for k in value:
            check(value[k], spec['properties'][k])
    elif kind == 'array':
        require(spec.get('minItems', 0) <= len(value) <= spec['maxItems'], 'Invalid array size.')
        for item in value:
            check(item, spec['items'])
        if spec.get('uniqueItems'):
            require(len(set(value)) == len(value), 'Repeated array values.')
    elif kind == 'integer':
        require(spec['minimum'] <= value <= spec['maximum'], 'Count outside bounds.')

def valid_metrics(m):
    t = m['tokens']
    require(t['total_tokens'] == t['input_tokens'] + t['output_tokens'], 'Token total does not reconcile.')
    require(t['cached_input_tokens'] <= t['input_tokens'], 'Cached input exceeds input.')
    require(t['reasoning_output_tokens'] <= t['output_tokens'], 'Reasoning exceeds output.')
    require(m['tasks_with_responses'] <= m['turns_with_responses'] <= m['responses'], 'Identity counts do not reconcile.')
    require(m['repository_contexts_with_responses'] <= m['responses'], 'Repository contexts exceed responses.')
    if m['responses'] == 0:
        require(not any(t.values()), 'Tokens without responses.')

def validate(data, ready=False):
    require(type(data) is dict, 'Submission must be an object.')
    version = data.get('schema_version')
    require(type(version) is str and version in SCHEMAS, 'Unsupported schema version.')
    check(data, json.loads(SCHEMAS[version].read_text()))
    valid_metrics(data['totals'])
    days = []
    for row in data['daily']:
        day = row['day_index']
        require(1 <= day <= data['window']['requested_days'], 'Daily row outside window.')
        days.append(day)
        valid_metrics(row)
    require(days == sorted(set(days)), 'Relative days must be unique and sorted.')
    for k in ('responses', 'native_user_message_items'):
        require(sum(x[k] for x in data['daily']) == data['totals'][k], 'Daily counts do not reconcile.')
    for k in data['totals']['tokens']:
        require(sum(x['tokens'][k] for x in data['daily']) == data['totals']['tokens'][k], 'Daily tokens do not reconcile.')
    for k in ('turns_with_responses','tasks_with_responses','repository_contexts_with_responses'):
        values = [x[k] for x in data['daily']]
        require(max(values, default=0) <= data['totals'][k] <= sum(values), 'Distinct identity partitions do not reconcile.')
    if 'self_reports' in data:
        valid_self_reports(data['self_reports'])
    if ready:
        require(all(data['consent'].values()), 'Explicit public release and MIT contribution consent required.')
    return data

def valid_self_reports(reports):
    timings = [group['timing'] for group in reports['groups']]
    require(len(timings) == len(set(timings)), 'Rating timing groups must be unique.')
    for group in reports['groups']:
        eligible, invited = group['eligible_task_attempts'], group['invited_task_attempts']
        recorded = len(group['ratings'])
        if eligible is not None:
            require(recorded <= eligible, 'Recorded rating attempts exceed eligibility.')
        if invited is not None:
            require(recorded <= invited, 'Recorded rating attempts exceed invitations.')
        if eligible is not None and invited is not None:
            require(invited <= eligible, 'Invitations exceed eligible attempts.')


def self_report_summary(reports):
    # Called only after validation. Do not combine timing groups or dimensions.
    groups = []
    for group in reports['groups']:
        invited, eligible = group['invited_task_attempts'], group['eligible_task_attempts']
        summary = {
            'timing': group['timing'],
            'eligible_task_attempts': eligible,
            'invited_task_attempts': invited,
            'recorded_task_attempts': len(group['ratings']),
        }
        for field, maximum in [('satisfaction', 5), ('task_ease', 7)]:
            counts = [sum(row[field] == score for row in group['ratings']) for score in range(1, maximum + 1)]
            answered = sum(counts)
            result = {
                'rating_counts_low_to_high': counts,
                'answered': answered,
                'recorded_unanswered': sum(row[field] is None for row in group['ratings']),
                'invited_without_answer': invited - answered if invited is not None else None,
                'response_coverage_percent': round(100 * answered / invited, 2) if invited else None,
                'eligible_coverage_percent': round(100 * answered / eligible, 2) if eligible else None,
            }
            if field == 'satisfaction':
                result['csat_percent'] = round(100 * sum(counts[3:]) / answered, 2) if answered else None
            summary[field] = result
        groups.append(summary)
    return {'protocol': reports['protocol'], 'participant_scope': reports['participant_scope'], 'groups': groups}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key rejected.')
        result[key] = value
    return result

def load(path):
    require(path.stat().st_size <= MAX_BYTES, 'Submission too large.')
    try:
        return json.loads(path.read_text(), object_pairs_hook=unique_object)
    except (ValueError, UnicodeError, RecursionError):
        raise ValidationError('Invalid JSON; no source content displayed.') from None

def preview(data):
    # Render only after full schema validation; never echo unsafe input or paths.
    validate(data)
    t = data['totals']
    result = {'synthetic': data['synthetic'], 'window': data['window'], 'setup': data['setup'], 'totals': t, 'observation_count': len(data['observations']), 'consent': data['consent']}
    if 'self_reports' in data:
        result['self_report_summary'] = self_report_summary(data['self_reports'])
    return json.dumps(result, indent=2)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('file', type=Path)
    p.add_argument('--ready', action='store_true', help='Require explicit release and license consent.')
    p.add_argument('--preview', action='store_true')
    a = p.parse_args()
    try:
        data = validate(load(a.file), ready=a.ready)
        print(preview(data) if a.preview else 'Valid allowlisted aggregate. Manual disclosure review still required.')
    except (ValidationError, OSError, RecursionError):
        print('Rejected: schema, accounting, consent or file check failed. No input content displayed.', file=sys.stderr)
        return 1
    return 0
if __name__ == '__main__':
    sys.exit(main())
