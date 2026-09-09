"""Closed, versioned observational evidence schema; separate from submissions."""
import json
from pathlib import Path

COUNT = {'type': 'integer', 'minimum': 0, 'maximum': 10**15}
DAY = {'type': 'integer', 'minimum': 1, 'maximum': 366}
PROJECT = {'type': 'string', 'enum': [f'Project {i:02}' for i in range(1, 100)]}
OBSERVER = {'type': 'string', 'enum': [f'Observer {i:02}' for i in range(1, 11)]}


def obj(properties):
    return {'type': 'object', 'additionalProperties': False,
            'required': list(properties), 'properties': properties}


def array(item, maximum=2000):
    return {'type': 'array', 'items': item, 'minItems': 0, 'maxItems': maximum}


def enum(*values):
    return {'type': 'string', 'enum': list(values)}


TOKEN_FIELDS = ('input_tokens', 'cached_input_tokens', 'uncached_input_tokens',
                'cache_write_input_tokens', 'output_tokens',
                'reasoning_output_tokens', 'total_tokens')
USAGE_FIELDS = ('responses', 'turns', 'completed_turns', 'incomplete_turns',
                'native_user_messages', 'tasks', 'sum_completed_turn_ms',
                'completed_interval_union_ms')
USAGE = {**{k: COUNT for k in USAGE_FIELDS},
         'tokens': obj({k: COUNT for k in TOKEN_FIELDS})}
PARTITION_FIELDS = ('eligible', 'D_only', 'C_only', 'both', 'routine', 'ambiguous',
                    'union', 'dissatisfaction_units', 'corrective_units')
EPISODE_FIELDS = ('correction_episodes', 'repeated_correction_episodes',
                  'process_correction_episodes', 'process_correction_units')
OUTCOMES = ('confirmed_resolved', 'accepted_with_residual_or_waived',
            'fix_reported_unverified', 'claim_withdrawn_artifact_unverified',
            'no_closure_established')
CODING = {**{k: COUNT for k in PARTITION_FIELDS + EPISODE_FIELDS},
          'outcomes': obj({k: COUNT for k in OUTCOMES})}
EVENT_FIELDS = (
    'issue_active_in_window', 'issue_active_state_closed', 'issue_active_state_open',
    'issue_candidate_records', 'issue_distinct_reopened',
    'issue_distinct_with_close_event', 'issue_opened_in_window', 'issue_window_events',
    'pr_active_in_window', 'pr_active_state_closed', 'pr_active_state_merged',
    'pr_active_state_open', 'pr_candidate_records', 'pr_distinct_reopened',
    'pr_distinct_with_close_event', 'pr_merged_in_window', 'pr_opened_in_window',
    'pr_window_events',
)
DIFF_FIELDS = ('added', 'deleted', 'binary_touches', 'file_touches', 'unique_paths')
CATEGORY_FIELDS = ('added', 'deleted', 'binary_touches', 'touches')
CATEGORIES = ('dependency_lock', 'documentation',
              'other_source_or_asset', 'test')
NET_SUMMARY_FIELDS = ('first_parent_commit_objects_in_window',
                     'net_changed_repository_qualified_paths', 'net_diff_additions',
                     'net_diff_deletions', 'repositories_with_complete_net_diff',
                     'repositories_with_default_branch_commit_activity')
SCHEMA = obj({
    'format': enum('observational_evidence'),
    'format_version': enum('1.0'),
    'synthetic': {'type': 'boolean'},
    'consent': obj({'public_release_reviewed': {'type': 'boolean'},
                    'mit_contribution': {'type': 'boolean'}}),
    'model': enum('gpt-6-astra'),
    'study_days': DAY,
    'direct_ratings': enum('not_collected'),
    'usage': obj({
        'summary': obj(USAGE),
        'by_day': array(obj({'day': DAY, **USAGE}), 366),
        'by_project': array(obj({'project': PROJECT, **USAGE}), 99),
        'by_observer': array(obj({'observer': OBSERVER, **USAGE}), 10),
        'by_day_project_observer': array(obj({'day': DAY, 'project': PROJECT,
                                             'observer': OBSERVER, **USAGE})),
    }),
    'coded_observations': obj({
        'protocol_version': enum('1.1'),
        'summary': obj(CODING),
        'by_day': array(obj({'day': DAY, **CODING}), 366),
        'by_project': array(obj({'project': PROJECT, **CODING}), 99),
        'by_day_project': array(obj({'day': DAY, 'project': PROJECT, **CODING})),
        'by_surface': array(obj({'surface': enum('typed', 'voice', 'voice_with_typed_reference'),
                                 **{k: COUNT for k in PARTITION_FIELDS}}), 3),
    }),
    'repository_activity': obj({
        'scope': enum('full_window_all_authors'),
        'identifiable_repositories': COUNT,
        'unresolved_projects': COUNT,
        'events': obj({k: COUNT for k in EVENT_FIELDS}),
        'net_changes': obj({**{k: COUNT for k in NET_SUMMARY_FIELDS},
                            'net_line_delta': {'type': 'integer', 'minimum': -10**15, 'maximum': 10**15}}),
        'by_project': array(obj({
            'project': PROJECT,
            'events': obj({k: COUNT for k in EVENT_FIELDS}),
            'first_parent_commit_objects_in_window': COUNT,
            'net_files_complete': {'type': 'boolean'},
            'net_diff': obj({**{k: COUNT for k in DIFF_FIELDS},
                             'categories': obj({k: obj({f: COUNT for f in CATEGORY_FIELDS}) for k in CATEGORIES})}),
        }), 99),
    }),
})
SCHEMA.update({'$schema': 'https://json-schema.org/draft/2020-12/schema',
               'title': 'Observational evidence 1.0 (not a contribution submission)'})

if __name__ == '__main__':
    destination = Path(__file__).resolve().parents[1] / 'schema/observational-evidence-v1.schema.json'
    destination.write_text(json.dumps(SCHEMA, indent=2) + '\n')
