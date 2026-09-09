"""Synthetic-only checks for the separate observational evidence contract."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from evidence_schema import (SCHEMA, USAGE_FIELDS, TOKEN_FIELDS, PARTITION_FIELDS,
                             EPISODE_FIELDS, OUTCOMES, EVENT_FIELDS, CATEGORIES,
                             CATEGORY_FIELDS)
from validate import ValidationError, load, validate
from validate_evidence import validate_evidence
from build_evidence_reader import reader_data


def fixture():
    """Invented two-project, one-day activity with overlapping runtime/tasks."""
    tokens = dict(input_tokens=100, cached_input_tokens=80, uncached_input_tokens=20,
                  cache_write_input_tokens=0, output_tokens=10, reasoning_output_tokens=4, total_tokens=110)
    unit = dict(responses=2, turns=1, completed_turns=1, incomplete_turns=0,
                native_user_messages=1, tasks=1, sum_completed_turn_ms=5000,
                completed_interval_union_ms=4000, tokens=tokens)
    total = {k: v * 2 for k, v in unit.items() if k != 'tokens'}
    total.update(tasks=1, completed_interval_union_ms=6000,
                 tokens={k: v * 2 for k, v in tokens.items()})
    empty = {**{k: 0 for k in PARTITION_FIELDS + EPISODE_FIELDS}, 'outcomes': {k: 0 for k in OUTCOMES}}
    corrected = copy.deepcopy(empty)
    corrected.update(eligible=1, both=1, union=1, dissatisfaction_units=1,
                     corrective_units=1, correction_episodes=1,
                     process_correction_episodes=1, process_correction_units=1)
    corrected['outcomes']['confirmed_resolved'] = 1
    routine = copy.deepcopy(empty)
    routine.update(eligible=1, routine=1)
    coded_total = {k: corrected[k] + routine[k] for k in PARTITION_FIELDS + EPISODE_FIELDS}
    coded_total['outcomes'] = copy.deepcopy(corrected['outcomes'])
    repo_rows = []
    for i in range(1, 3):
        events = {k: 0 for k in EVENT_FIELDS}
        if i == 1:
            for kind in ('issue', 'pr'):
                for suffix in ('active_in_window', 'candidate_records', 'opened_in_window', 'distinct_with_close_event'):
                    events[kind + '_' + suffix] = 1
                events[kind + '_window_events'] = 3
            events['issue_active_state_closed'] = 1
            events['pr_active_state_merged'] = 1
            events['pr_merged_in_window'] = 1
        categories = {k: {f: 0 for f in CATEGORY_FIELDS} for k in CATEGORIES}
        categories['documentation'].update(added=10, deleted=1, touches=1)
        repo_rows.append({'project': f'Project {i:02}', 'events': events,
                          'first_parent_commit_objects_in_window': 1, 'net_files_complete': True,
                          'net_diff': dict(added=10, deleted=1, binary_touches=0, file_touches=1,
                                           unique_paths=1, categories=categories)})
    return {
        'format': 'observational_evidence', 'format_version': '1.0', 'synthetic': True,
        'consent': {'public_release_reviewed': True, 'mit_contribution': True},
        'model': 'gpt-6-astra', 'study_days': 1, 'direct_ratings': 'not_collected',
        'usage': {'summary': copy.deepcopy(total), 'by_day': [{'day': 1, **copy.deepcopy(total)}],
                  'by_project': [{'project': f'Project {i:02}', **copy.deepcopy(unit)} for i in (1, 2)],
                  'by_observer': [{'observer': 'Observer 01', **copy.deepcopy(total)}],
                  'by_day_project_observer': [{'day': 1, 'project': f'Project {i:02}', 'observer': 'Observer 01',
                                               **copy.deepcopy(unit)} for i in (1, 2)]},
        'coded_observations': {'protocol_version': '1.1', 'summary': coded_total,
            'by_day': [{'day': 1, **copy.deepcopy(coded_total)}],
            'by_project': [{'project': f'Project {i:02}', **copy.deepcopy(v)} for i, v in [(1, corrected), (2, routine)]],
            'by_day_project': [{'day': 1, 'project': f'Project {i:02}', **copy.deepcopy(v)} for i, v in [(1, corrected), (2, routine)]],
            'by_surface': [{'surface': 'typed', **{k: coded_total[k] for k in PARTITION_FIELDS}}]},
        'repository_activity': {'scope': 'full_window_all_authors', 'identifiable_repositories': 2, 'unresolved_projects': 0,
            'events': {k: sum(x['events'][k] for x in repo_rows) for k in EVENT_FIELDS},
            'net_changes': dict(first_parent_commit_objects_in_window=2, net_changed_repository_qualified_paths=2,
                                net_diff_additions=20, net_diff_deletions=2, net_line_delta=18,
                                repositories_with_complete_net_diff=2, repositories_with_default_branch_commit_activity=2),
            'by_project': repo_rows},
    }


class EvidenceTests(unittest.TestCase):
    def rejects(self, data):
        with self.assertRaises(ValidationError):
            validate_evidence(data)

    def test_valid_nonadditive_groups_and_unchanged_submission_contracts(self):
        data = fixture()
        validate_evidence(data, ready=True)
        self.assertLess(data['usage']['summary']['completed_interval_union_ms'],
                        sum(x['completed_interval_union_ms'] for x in data['usage']['by_project']))
        self.assertEqual(data['usage']['summary']['tasks'], 1)
        self.assertEqual(sum(x['tasks'] for x in data['usage']['by_project']), 2)
        self.assertEqual(json.loads((ROOT / 'schema/observational-evidence-v1.schema.json').read_text()), SCHEMA)
        for name in ('synthetic-submission.json', 'synthetic-ratings-submission.json'):
            validate(load(ROOT / 'examples' / name), ready=True)
        with self.assertRaises(ValidationError):
            validate(data)  # Evidence is deliberately not accepted as a submission.

    def test_unknown_fields_rejected_at_every_object_level(self):
        def paths(value, path=()):
            if isinstance(value, dict):
                yield path
                for k, v in value.items():
                    yield from paths(v, path + (k,))
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    yield from paths(v, path + (i,))
        for path in paths(fixture()):
            data = fixture()
            target = data
            for key in path:
                target = target[key]
            target['private_note'] = 'SYNTHETIC_PRIVATE_SENTINEL'
            with self.subTest(path=path):
                self.rejects(data)

    def test_accounting_and_invalid_count_types(self):
        for field in TOKEN_FIELDS:
            for value in (True, -1, 1.5, 'SYNTHETIC_PRIVATE_SENTINEL', 10**16):
                data = fixture()
                data['usage']['summary']['tokens'][field] = value
                with self.subTest(field=field, value_type=type(value).__name__):
                    self.rejects(data)
        for field in ('total_tokens', 'uncached_input_tokens', 'reasoning_output_tokens'):
            data = fixture()
            data['usage']['summary']['tokens'][field] = 1000
            self.rejects(data)
        for field in ('turns', 'sum_completed_turn_ms', 'completed_interval_union_ms', 'tasks'):
            data = fixture()
            data['usage']['summary'][field] = 100000
            self.rejects(data)

    def test_group_keys_and_cross_group_accounting(self):
        for mutation in ('duplicate', 'outside_day', 'unknown_project', 'unknown_observer', 'cross_group'):
            data = fixture()
            cube = data['usage']['by_day_project_observer']
            if mutation == 'duplicate':
                cube.append(copy.deepcopy(cube[0]))
            elif mutation == 'outside_day':
                cube[0]['day'] = 2
            elif mutation == 'unknown_project':
                cube[0]['project'] = 'Project 03'
            elif mutation == 'unknown_observer':
                cube[0]['observer'] = 'Observer 02'
            else:
                cube[0]['responses'] += 1
                cube[1]['responses'] -= 1  # Overall total stays correct; project partitions do not.
            with self.subTest(mutation=mutation):
                self.rejects(data)

    def test_overlap_episodes_and_surface_partition(self):
        for field in ('eligible', 'both', 'union', 'corrective_units', 'dissatisfaction_units',
                      'correction_episodes', 'repeated_correction_episodes', 'process_correction_units'):
            data = fixture()
            data['coded_observations']['summary'][field] += 10
            self.rejects(data)
        data = fixture()
        data['coded_observations']['by_surface'][0]['routine'] += 1
        self.rejects(data)
        data = fixture()
        data['coded_observations']['by_day_project'][0]['project'] = 'Project 03'
        self.rejects(data)
        data = fixture()
        data['coded_observations']['summary']['outcomes']['no_closure_established'] += 1
        self.rejects(data)

    def test_repository_states_diffs_and_missingness(self):
        for mutation in ('coverage', 'unknown_project', 'state', 'delta', 'category', 'completeness'):
            data = fixture()
            repo = data['repository_activity']
            if mutation == 'coverage':
                repo['unresolved_projects'] = 1
            elif mutation == 'unknown_project':
                repo['by_project'][0]['project'] = 'Project 03'
            elif mutation == 'state':
                repo['by_project'][0]['events']['pr_active_state_open'] = 1
            elif mutation == 'delta':
                repo['net_changes']['net_line_delta'] += 1
            elif mutation == 'category':
                repo['by_project'][0]['net_diff']['categories']['documentation']['added'] += 1
            else:
                repo['by_project'][0]['net_files_complete'] = False
            self.rejects(data)

    def test_ratings_and_identifying_vocabulary_rejected(self):
        for field, value in [('direct_ratings', 'inferred'), ('model', 'SYNTHETIC_PRIVATE_SENTINEL'),
                              ('format_version', '1.1'), ('format', 'submission')]:
            data = fixture()
            data[field] = value
            self.rejects(data)
        data = fixture()
        data['usage']['by_project'][0]['project'] = 'SYNTHETIC_PRIVATE_SENTINEL'
        self.rejects(data)

    def test_reader_is_a_controlled_derivative_with_missing_cells(self):
        data = fixture()
        derived = reader_data(data)
        self.assertTrue(derived['synthetic'])
        self.assertEqual(len(derived['rows']), 2)
        self.assertEqual(sum(x['responses'] for x in derived['rows']), 4)
        self.assertEqual(sum(x['corrective_units'] for x in derived['rows']), 1)
        self.assertEqual(sum(x['total_tokens'] for x in derived['rows']), 220)
        self.assertEqual(sum(x['merged'] for x in derived['repository']), 1)
        for row in derived['rows']:
            self.assertNotIn('observer', row)
            self.assertNotIn('tasks', row)
            self.assertNotIn('completed_interval_union_ms', row)
            self.assertEqual(row['eligible'], sum(row[k] for k in ('D_only', 'C_only', 'both', 'routine', 'ambiguous')))
        # Removing a fully zero event row still requires matching coverage/net summaries.
        # Missing repository history is represented by absence, not an invented zero row.
        self.assertEqual([x['project'] for x in derived['repository']], ['Project 01', 'Project 02'])

    def test_consent_duplicate_json_and_redacted_cli(self):
        data = fixture()
        data['consent']['public_release_reviewed'] = False
        validate_evidence(data)
        with self.assertRaises(ValidationError):
            validate_evidence(data, ready=True)
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / 'SYNTHETIC_PRIVATE_PATH.json'
            data['private_source'] = 'SYNTHETIC_PRIVATE_SENTINEL'
            file.write_text(json.dumps(data))
            result = subprocess.run([sys.executable, str(ROOT / 'tools/validate_evidence.py'), str(file)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('SYNTHETIC_PRIVATE', result.stdout + result.stderr)
            file.write_text('{"format": "observational_evidence", "format": "observational_evidence"}')
            with self.assertRaises(ValidationError):
                load(file)


if __name__ == '__main__':
    unittest.main()
