"""Synthetic-only tests for optional direct ratings and privacy boundaries."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate import load, preview, validate, ValidationError
from make_schema import schema, schema_v11


class RatingTests(unittest.TestCase):
    def example(self):
        return load(ROOT / 'examples/synthetic-ratings-submission.json')

    def test_old_contract_and_new_optional_layer(self):
        old = load(ROOT / 'examples/synthetic-submission.json')
        validate(old, ready=True)
        self.assertEqual(old['schema_version'], '1.0')
        self.assertNotIn('self_reports', old)
        old['schema_version'] = '1.1'
        validate(old, ready=True)
        upgraded = self.example()
        validate(upgraded, ready=True)
        upgraded['schema_version'] = '1.0'
        with self.assertRaises(ValidationError):
            validate(upgraded)
        self.assertEqual(load(ROOT / 'schema/submission-v1.schema.json'), schema)
        self.assertEqual(load(ROOT / 'schema/submission-v1.1.schema.json'), schema_v11)

    def test_rating_boundaries_nulls_and_invalid_types(self):
        for field, maximum in [('satisfaction', 5), ('task_ease', 7)]:
            for value in [None, 1, maximum]:
                with self.subTest(field=field, valid=value):
                    data = self.example()
                    data['self_reports']['groups'][0]['ratings'][0][field] = value
                    validate(data)
            for value in [0, -1, maximum + 1, True, False, 1.5, '5', [], {}]:
                with self.subTest(field=field, invalid=value):
                    data = self.example()
                    data['self_reports']['groups'][0]['ratings'][0][field] = value
                    with self.assertRaises(ValidationError):
                        validate(data)

    def test_denominators_unknown_zero_and_inconsistent(self):
        for eligible, invited, valid in [
            (None, None, True), (None, 4, True), (4, None, True), (5, 4, True),
            (0, None, False), (None, 0, False), (3, 4, False), (10, 3, False),
            (3, None, False), (4, 5, False), (True, None, False), (None, -1, False),
        ]:
            with self.subTest(eligible=eligible, invited=invited):
                data = self.example()
                group = data['self_reports']['groups'][0]
                group['eligible_task_attempts'] = eligible
                group['invited_task_attempts'] = invited
                if valid:
                    validate(data)
                else:
                    with self.assertRaises(ValidationError):
                        validate(data)
        data = self.example()
        data['self_reports']['groups'] = [{
            'timing': 'unknown', 'eligible_task_attempts': 0,
            'invited_task_attempts': 0, 'ratings': [],
        }]
        result = json.loads(preview(data))['self_report_summary']['groups'][0]
        self.assertEqual(result['satisfaction']['answered'], 0)
        self.assertIsNone(result['satisfaction']['csat_percent'])
        self.assertIsNone(result['task_ease']['response_coverage_percent'])
        self.assertEqual(result['satisfaction']['invited_without_answer'], 0)

    def test_distributions_csat_and_coverage_remain_separate(self):
        groups = json.loads(preview(self.example()))['self_report_summary']['groups']
        immediate, recalled = groups
        self.assertEqual(immediate['satisfaction']['rating_counts_low_to_high'], [0, 1, 0, 1, 1])
        self.assertEqual(immediate['satisfaction']['answered'], 3)
        self.assertEqual(immediate['satisfaction']['csat_percent'], 66.67)
        self.assertEqual(immediate['satisfaction']['response_coverage_percent'], 60.0)
        self.assertEqual(immediate['satisfaction']['eligible_coverage_percent'], 37.5)
        self.assertEqual(immediate['satisfaction']['recorded_unanswered'], 1)
        self.assertEqual(immediate['satisfaction']['invited_without_answer'], 2)
        self.assertEqual(immediate['task_ease']['rating_counts_low_to_high'], [0, 1, 0, 0, 0, 1, 0])
        self.assertEqual(immediate['task_ease']['response_coverage_percent'], 40.0)
        self.assertNotIn('csat_percent', immediate['task_ease'])
        self.assertEqual(recalled['satisfaction']['csat_percent'], 0.0)
        self.assertIsNone(recalled['satisfaction']['response_coverage_percent'])
        self.assertIsNone(recalled['satisfaction']['invited_without_answer'])
        self.assertEqual(recalled['satisfaction']['rating_counts_low_to_high'], [1, 0, 0, 0, 0])

    def test_unanswered_is_not_neutral_or_satisfied(self):
        data = self.example()
        group = data['self_reports']['groups'][0]
        group['ratings'] = [{'satisfaction': None, 'task_ease': None}]
        group['invited_task_attempts'] = 2
        result = json.loads(preview(data))['self_report_summary']['groups'][0]
        self.assertEqual(result['satisfaction']['rating_counts_low_to_high'], [0] * 5)
        self.assertEqual(result['task_ease']['rating_counts_low_to_high'], [0] * 7)
        self.assertIsNone(result['satisfaction']['csat_percent'])
        self.assertEqual(result['satisfaction']['response_coverage_percent'], 0.0)
        self.assertEqual(result['satisfaction']['invited_without_answer'], 2)

    def test_timing_protocol_and_participant_vocabulary(self):
        for timing in ['immediately_after_task', 'retrospective_recollection', 'unknown']:
            data = self.example()
            data['self_reports']['groups'] = [data['self_reports']['groups'][0]]
            data['self_reports']['groups'][0]['timing'] = timing
            validate(data)
        for mutation in ['duplicate', 'invalid_timing', 'no_groups', 'protocol', 'participant', 'null_layer']:
            data = self.example()
            reports = data['self_reports']
            if mutation == 'duplicate':
                reports['groups'][1]['timing'] = reports['groups'][0]['timing']
            elif mutation == 'invalid_timing':
                reports['groups'][0]['timing'] = '2026-09-01T12:00:00Z'
            elif mutation == 'no_groups':
                reports['groups'] = []
            elif mutation == 'protocol':
                reports['protocol'] = 'inferred_from_transcripts'
            elif mutation == 'participant':
                reports['participant_scope'] = 'multiple_people'
            else:
                data['self_reports'] = None
            with self.subTest(mutation=mutation), self.assertRaises(ValidationError):
                validate(data)

    def test_identifying_fields_rejected_at_every_new_level(self):
        for level in ['reports', 'group', 'rating']:
            for key in ['task_id', 'timestamp', 'repository', 'machine', 'notes', 'source_hash']:
                data = self.example()
                reports = data['self_reports']
                target = {'reports': reports, 'group': reports['groups'][0],
                          'rating': reports['groups'][0]['ratings'][0]}[level]
                target[key] = 'SYNTHETIC_PRIVATE_SENTINEL'
                with self.subTest(level=level, key=key), self.assertRaises(ValidationError):
                    validate(data)
        data = self.example()
        del data['self_reports']['groups'][0]['ratings'][0]['satisfaction']
        with self.assertRaises(ValidationError):
            validate(data)  # Missingness must be explicit null, not omitted.

    def test_rating_consent_canonicalization_and_redacted_cli(self):
        data = self.example()
        data['consent']['public_release_reviewed'] = False
        with self.assertRaises(ValidationError):
            validate(data, ready=True)
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'clean.json'
            completed = subprocess.run([
                sys.executable, str(ROOT / 'tools/sanitize.py'),
                str(ROOT / 'examples/synthetic-ratings-submission.json'), '--out', str(target),
            ], text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(load(target), self.example())
            private = Path(temp) / 'private.json'
            data['self_reports']['groups'][0]['ratings'][0]['satisfaction'] = 'SYNTHETIC_PRIVATE_SENTINEL'
            private.write_text(json.dumps(data))
            completed = subprocess.run([
                sys.executable, str(ROOT / 'tools/validate.py'), str(private), '--preview',
            ], text=True, capture_output=True)
            self.assertNotEqual(completed.returncode, 0)
            self.assertNotIn('SYNTHETIC_PRIVATE_SENTINEL', completed.stdout + completed.stderr)
            self.assertNotIn(str(private), completed.stdout + completed.stderr)


if __name__ == '__main__':
    unittest.main()
