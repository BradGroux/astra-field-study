#!/usr/bin/env python3
"""Read local native Codex records; emit only schema-validated aggregate counts."""
import argparse
from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone
import json
from pathlib import Path
import sys
from validate import ValidationError, require, validate, preview
from make_schema import TOKENS

MODELS = ('gpt-6-astra','gpt-5.6-sol','gpt-5.6-terra','gpt-5.6-luna','gpt-5.5')

def timestamp(value):
    require(isinstance(value, str), 'Missing timestamp.')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.tzinfo is not None, 'Timezone required.')
    return result.astimezone(timezone.utc)

def identity(value):
    require(isinstance(value,str) and bool(value), 'Missing native identity.')
    return value

def token_counts(raw):
    require(isinstance(raw, dict) and set(raw) == set(TOKENS), 'Unsupported token fields.')
    require(all(type(v) is int and 0 <= v <= 10**15 for v in raw.values()), 'Invalid token counts.')
    require(raw['total_tokens'] == raw['input_tokens'] + raw['output_tokens'], 'Invalid token arithmetic.')
    require(raw['cached_input_tokens'] <= raw['input_tokens'] and raw['reasoning_output_tokens'] <= raw['output_tokens'], 'Invalid token subsets.')
    return dict(raw)

def aggregate(home, start, end, model, client='unknown', effort='unknown'):
    require(model in MODELS, 'Unsupported model.')
    first = datetime.combine(date.fromisoformat(start), time.min, timezone.utc)
    stop = datetime.combine(date.fromisoformat(end)+timedelta(days=1), time.min, timezone.utc)
    require(0 < (stop-first).days <= 366, 'Invalid window.')
    require(first.date() <= datetime.now(timezone.utc).date(), 'Future start date.')
    roots = [home/'sessions', home/'archived_sessions']
    paths = sorted(set(p for root in roots for p in root.rglob('*.jsonl')))
    require(bool(paths), 'No retained JSONL files.')
    # Freeze byte boundaries. A local live store is not an atomic cross-file snapshot.
    require(not any(p.is_symlink() for p in paths) and not any(r.is_symlink() for r in roots), 'Symlinked input not supported.')
    manifest = [(p,p.stat().st_size) for p in paths]
    contexts = defaultdict(set)
    repositories = {}
    records, messages = [], []
    snapshots = 0
    for path, size in manifest:
        owner = None
        repository = None
        with path.open('rb') as stream:
            consumed = 0
            while consumed < size:
                line = stream.readline(size-consumed)
                consumed += len(line)
                require(bool(line) and line.endswith(b'\n'), 'Partial snapshot; retry after active writes stop.')
                row = json.loads(line)
                require(isinstance(row,dict), 'Unsupported record shape.')
                kind = row.get('type')
                if kind not in ('session_meta','turn_context','token_usage_record','event_msg'):
                    continue
                payload = row.get('payload')
                require(isinstance(payload,dict), 'Unsupported payload.')
                when = timestamp(row.get('timestamp'))
                if when >= stop:
                    continue
                if kind == 'session_meta':
                    owner = identity(payload.get('id'))
                    git = payload.get('git') or {}
                    repository = git.get('repository_url') or payload.get('cwd')
                    require(repository is None or isinstance(repository,str), 'Unsupported repository context.')
                    require(owner not in repositories or repositories[owner] == repository, 'Conflicting repository context.')
                    repositories[owner] = repository
                elif kind == 'turn_context':
                    turn = payload.get('turn_id')
                    if turn:
                        contexts[identity(turn)].add(payload.get('model'))
                elif kind == 'token_usage_record':
                    # Copy only the required metadata; never retain prompt/tool text.
                    records.append((when, payload.get('response_id'), payload.get('turn_id'), payload.get('thread_id'), payload.get('usage')))
                elif payload.get('type') == 'item_completed' and (payload.get('item') or {}).get('type') == 'UserMessage':
                    messages.append((when,payload.get('item',{}).get('id'),payload.get('turn_id'),payload.get('thread_id',owner)))
                elif payload.get('type') == 'token_count' and first <= when < stop:
                    snapshots += 1
    require(not any(model in models and models != {model} for models in contexts.values()), 'Ambiguous model attribution; export refused.')
    selected = {turn for turn, models in contexts.items() if models == {model}}
    responses = {}
    duplicates = 0
    for when, rid, turn, thread, usage in records:
        if turn not in selected:
            # Native usage without explicit matching model context is never inferred.
            require(turn in contexts, 'Usage without matching turn context; export refused.')
            continue
        key = identity(rid)
        current = (when, identity(turn), identity(thread), token_counts(usage), repositories.get(thread))
        if key in responses:
            prior = responses[key]
            require(prior[1:4] == current[1:4], 'Conflicting response replay; export refused.')
            duplicates += int(first <= when < stop)
            if when < prior[0]:
                responses[key] = current
        else:
            responses[key] = current
    responses = {k:v for k,v in responses.items() if first <= v[0] < stop}
    require(bool(responses), 'No supported native response records in window.')
    owners = {v[1]:v[2] for v in responses.values()}
    require(all(owners[v[1]] == v[2] for v in responses.values()), 'Conflicting turn owner.')
    native = {}
    for when, item, turn, thread in messages:
        if turn not in owners:
            continue
        require(identity(thread) == owners[turn], 'Conflicting message owner.')
        key = identity(item)
        value = (when, turn, thread)
        if key in native:
            require(native[key][1:] == value[1:], 'Conflicting message replay.')
            native[key] = min(native[key], value)
        else:
            native[key] = value
    native = {k:v for k,v in native.items() if first <= v[0] < stop}
    def summarize(rs, ms):
        return {'responses':len(rs), 'turns_with_responses':len({v[1] for v in rs}), 'tasks_with_responses':len({v[2] for v in rs}), 'native_user_message_items':len(ms), 'repository_contexts_with_responses':len({v[4] for v in rs if v[4] is not None}), 'tokens':{k:sum(v[3][k] for v in rs) for k in TOKENS}}
    days = sorted({v[0].date().isoformat() for v in responses.values()} | {v[0].date().isoformat() for v in native.values()})
    data = {'schema_version':'1.0', 'synthetic':False, 'consent':{'public_release_reviewed':False,'rights_and_mit_license_confirmed':False}, 'setup':{'model':model,'attribution':'recorded_turn_context','client':client,'reasoning_effort':effort,'observer_scope':'one_local_store','collection_format':'codex_native_response_records_v1'}, 'window':{'requested_days':(stop-first).days}, 'totals':summarize(list(responses.values()),list(native.values())), 'daily':[{'day_index':(date.fromisoformat(day)-first.date()).days+1,**summarize([v for v in responses.values() if v[0].date().isoformat()==day],[v for v in native.values() if v[0].date().isoformat()==day])} for day in days], 'diagnostics':{'duplicate_response_records':duplicates,'ignored_counter_snapshots':snapshots}, 'observations':[]}
    return validate(data)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--home',type=Path,default=Path.home()/'.codex')
    p.add_argument('--start',required=True,help='First UTC date, YYYY-MM-DD.')
    p.add_argument('--end',required=True,help='Last UTC date, inclusive.')
    p.add_argument('--model',choices=MODELS,default='gpt-6-astra')
    p.add_argument('--client',choices=('codex_desktop','codex_cli','mixed','unknown'),default='unknown')
    p.add_argument('--effort',choices=('low','medium','high','xhigh','max','ultra','mixed','unknown'),default='unknown')
    p.add_argument('--out',type=Path,required=True,help='New local draft file outside this checkout and the source store.')
    a = p.parse_args()
    try:
        out = a.out.resolve()
        source = a.home.resolve()
        checkout = Path(__file__).resolve().parents[1]
        require(not out.is_relative_to(source) and not out.is_relative_to(checkout), 'Draft must stay outside source store and checkout.')
        data = aggregate(source,a.start,a.end,a.model,a.client,a.effort)
        with out.open('x',encoding='utf-8') as stream:
            stream.write(json.dumps(data,indent=2)+'\n')
        print(preview(data))
        print('Local draft only. Review the entire JSON before giving release consent. Nothing was uploaded.')
    except (ValidationError, ValueError, TypeError, AttributeError, KeyError, OSError, RecursionError):
        print('Collection refused: unsupported, inconsistent or unavailable local records/output. No source content displayed.',file=sys.stderr)
        return 1
    return 0
if __name__ == '__main__':
    sys.exit(main())
