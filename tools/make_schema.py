"""Regenerate the submission contract; no dependencies."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def obj(properties):
    return {'type': 'object', 'additionalProperties': False, 'required': list(properties), 'properties': properties}
def choice(*values):
    return {'type': 'string', 'enum': list(values)}
def count():
    return {'type': 'integer', 'minimum': 0, 'maximum': 10**15}
def array(items, maximum=366):
    return {'type': 'array', 'items': items, 'maxItems': maximum}
TOKENS = ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens', 'output_tokens', 'reasoning_output_tokens', 'total_tokens')
COUNTS = ('responses', 'turns_with_responses', 'tasks_with_responses', 'native_user_message_items', 'repository_contexts_with_responses')
tokens = obj({k: count() for k in TOKENS})
metrics = obj({**{k: count() for k in COUNTS}, 'tokens': tokens})
observation = obj({
    'requirement': choice('run_local_checks', 'respect_scope', 'follow_documented_steps', 'preserve_user_work', 'verify_outcome', 'follow_delegation_limit'),
    'behavior': choice('followed_requirement', 'omitted_required_step', 'changed_required_process', 'lost_requirement_after_handoff', 'requested_clarification', 'insufficient_evidence'),
    'delegation': choice('none', 'used', 'unknown'),
    'instruction_access': choice('confirmed_in_recipient_context', 'available_but_read_unconfirmed', 'absent_from_handoff', 'unknown'),
    'result': choice('verified_success', 'deviation_corrected', 'unresolved_deviation', 'inconclusive'),
    'evidence_basis': choice('local_action_and_outcome_review', 'local_action_review_only', 'recollection_only'),
    'alternatives_considered': {**array(choice('ambiguous_requirement', 'missing_context', 'tool_limitation', 'client_or_harness_behavior', 'task_difficulty', 'human_error', 'unknown'), 7), 'uniqueItems': True, 'minItems': 1},
})
schema = {
 '$schema': 'https://json-schema.org/draft/2020-12/schema',
 '$id': 'https://github.com/BradGroux/astra-field-study/blob/main/schema/submission-v1.schema.json',
 'title': 'Astra Field Study sanitized aggregate submission v1',
 **obj({
 'schema_version': choice('1.0'), 'synthetic': {'type': 'boolean'},
 'consent': obj({'public_release_reviewed': {'type': 'boolean'}, 'rights_and_mit_license_confirmed': {'type': 'boolean'}}),
 'setup': obj({'model': choice('gpt-6-astra', 'gpt-5.6-sol', 'gpt-5.6-terra', 'gpt-5.6-luna', 'gpt-5.5'), 'attribution': choice('recorded_turn_context'), 'client': choice('codex_desktop', 'codex_cli', 'mixed', 'unknown'), 'reasoning_effort': choice('low','medium','high','xhigh','max','ultra','mixed','unknown'), 'observer_scope': choice('one_local_store'), 'collection_format': choice('codex_native_response_records_v1')}),
 'window': obj({'requested_days': {'type':'integer','minimum':1,'maximum':366}}),
 'totals': metrics,
 'daily': array(obj({'day_index': {'type':'integer','minimum':1,'maximum':366}, **metrics['properties']})),
 'diagnostics': obj({'duplicate_response_records': count(), 'ignored_counter_snapshots': count()}),
 'observations': array(observation, 100),
 })}
if __name__ == '__main__':
 (ROOT/'schema/submission-v1.schema.json').write_text(json.dumps(schema, indent=2)+'\n')
