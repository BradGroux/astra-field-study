import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from collect import aggregate
from validate import validate, load, ValidationError

STAMP='2026-09-01T12:00:00Z'
def row(kind,payload,stamp=STAMP):
    return {'timestamp':stamp,'type':kind,'payload':payload}
def fixture(model='gpt-6-astra'):
    counts={'input_tokens':100,'cached_input_tokens':80,'cache_write_input_tokens':0,'output_tokens':10,'reasoning_output_tokens':4,'total_tokens':110}
    return [row('session_meta',{'id':'synthetic-task','cwd':'/synthetic/private-project','git':{'repository_url':'https://example.invalid/private-repo'}}),row('turn_context',{'turn_id':'synthetic-turn','model':model}),row('response_item',{'content':'SYNTHETIC_SECRET_SENTINEL'}),row('token_usage_record',{'response_id':'synthetic-response','turn_id':'synthetic-turn','thread_id':'synthetic-task','session_id':'different-root-session','usage':counts}),row('event_msg',{'type':'token_count','info':{'total_token_usage':counts}}),row('event_msg',{'type':'item_completed','thread_id':'synthetic-task','turn_id':'synthetic-turn','item':{'id':'synthetic-message','type':'UserMessage','content':'SYNTHETIC_SECRET_SENTINEL'}})]
class KitTests(unittest.TestCase):
    def run_fixture(self,rows,second=None):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d);(home/'sessions').mkdir()
            (home/'sessions/a.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
            if second is not None:
                (home/'sessions/b.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in second))
            return aggregate(home,'2026-09-01','2026-09-02','gpt-6-astra')
    def test_accounting_and_no_private_fields(self):
        data=self.run_fixture(fixture())
        self.assertEqual(data['totals']['tokens']['total_tokens'],110)
        self.assertEqual(data['totals']['native_user_message_items'],1)
        self.assertEqual(data['diagnostics']['ignored_counter_snapshots'],1)
        for secret in ('SYNTHETIC_SECRET_SENTINEL','private-project','private-repo','synthetic-task','synthetic-response','different-root-session'):
            self.assertNotIn(secret,json.dumps(data))
        self.assertFalse(data['consent']['public_release_reviewed'])
    def test_replay_deduplication(self):
        data=self.run_fixture(fixture(),fixture())
        self.assertEqual(data['totals']['responses'],1)
        self.assertEqual(data['totals']['native_user_message_items'],1)
        self.assertEqual(data['diagnostics']['duplicate_response_records'],1)
    def test_conflicting_replay_fails(self):
        second=fixture();second[3]['payload']['usage']['input_tokens']=101;second[3]['payload']['usage']['total_tokens']=111
        with self.assertRaises(ValidationError):self.run_fixture(fixture(),second)
    def test_context_model_not_session_setting(self):
        rows=fixture();rows[0]['payload']['model']='gpt-5.5'
        self.assertEqual(self.run_fixture(rows)['totals']['responses'],1)
        with self.assertRaises(ValidationError):self.run_fixture(fixture('gpt-5.5'))
    def test_ambiguous_and_missing_context_fail(self):
        rows=fixture()+[row('turn_context',{'turn_id':'synthetic-turn','model':'gpt-5.5'})]
        with self.assertRaises(ValidationError):self.run_fixture(rows)
        with self.assertRaises(ValidationError):self.run_fixture([x for x in fixture() if x['type']!='turn_context'])
    def test_snapshot_only_not_responses(self):
        with self.assertRaises(ValidationError):self.run_fixture([x for x in fixture() if x['type']!='token_usage_record'])
    def test_bad_components_fail(self):
        for mutate in ('total','subset','bool','missing'):
            rows=fixture();t=rows[3]['payload']['usage']
            if mutate=='total':t['total_tokens']=999
            if mutate=='subset':t['cached_input_tokens']=101
            if mutate=='bool':t['reasoning_output_tokens']=True
            if mutate=='missing':del t['cached_input_tokens']
            with self.subTest(mutate=mutate),self.assertRaises(ValidationError):self.run_fixture(rows)
    def test_daily_cross_day_identity_counts(self):
        rows=fixture();other=copy.deepcopy(rows[3]);other['timestamp']='2026-09-02T01:00:00Z';other['payload']['response_id']='synthetic-second';rows.append(other)
        data=self.run_fixture(rows)
        self.assertEqual(data['totals']['turns_with_responses'],1)
        self.assertEqual(sum(x['turns_with_responses'] for x in data['daily']),2)
        self.assertEqual(data['totals']['tokens']['total_tokens'],220)
    def test_private_fields_rejected_at_any_level(self):
        data=self.run_fixture(fixture())
        for target in ('root','tokens','setup','daily'):
            d=copy.deepcopy(data);obj={'root':d,'tokens':d['totals']['tokens'],'setup':d['setup'],'daily':d['daily'][0]}[target]
            obj['secret']='SYNTHETIC_SECRET_SENTINEL'
            with self.subTest(target=target),self.assertRaises(ValidationError):validate(d)
        d=copy.deepcopy(data);d['setup']['client']='/private/path'
        with self.assertRaises(ValidationError):validate(d)
    def test_consent_and_daily_integrity(self):
        d=self.run_fixture(fixture())
        with self.assertRaises(ValidationError):validate(d,ready=True)
        d['consent']={k:True for k in d['consent']};validate(d,ready=True)
        d['daily']=[]
        with self.assertRaises(ValidationError):validate(d)
    def test_duplicate_json_keys_and_error_redaction(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'candidate.json';f.write_text('{"schema_version":"1.0","schema_version":"SYNTHETIC_SECRET_SENTINEL"}')
            with self.assertRaises(ValidationError):load(f)
            p=subprocess.run([sys.executable,str(ROOT/'tools/validate.py'),str(f)],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0);self.assertNotIn('SYNTHETIC_SECRET_SENTINEL',p.stdout+p.stderr);self.assertNotIn(str(f),p.stdout+p.stderr)
    def test_example_and_canonicalization(self):
        d=load(ROOT/'examples/synthetic-submission.json');validate(d,ready=True)
        self.assertTrue(d['synthetic']);self.assertTrue(any(x['behavior']=='followed_requirement' for x in d['observations']))
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'clean.json'
            p=subprocess.run([sys.executable,str(ROOT/'tools/sanitize.py'),str(ROOT/'examples/synthetic-submission.json'),'--out',str(target)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(load(target),d)
            p=subprocess.run([sys.executable,str(ROOT/'tools/sanitize.py'),str(ROOT/'examples/synthetic-submission.json'),'--out',str(target)],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
    def test_cli_collection_creates_reviewable_draft_only(self):
        with tempfile.TemporaryDirectory() as d:
            parent=Path(d);home=parent/'store';(home/'sessions').mkdir(parents=True)
            (home/'sessions/a.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in fixture()))
            out=parent/'draft.json'
            args=[sys.executable,str(ROOT/'tools/collect.py'),'--home',str(home),'--start','2026-09-01','--end','2026-09-02','--out',str(out)]
            p=subprocess.run(args,capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            data=validate(load(out));self.assertFalse(any(data['consent'].values()))
            for forbidden in ('2026-09-01','synthetic-task','private-project','SYNTHETIC_SECRET_SENTINEL'):
                self.assertNotIn(forbidden,out.read_text()+p.stdout+p.stderr)
            original=out.read_bytes()
            p=subprocess.run(args,capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0);self.assertEqual(out.read_bytes(),original)
            args[-1]=str(home/'unsafe.json')
            p=subprocess.run(args,capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0);self.assertFalse((home/'unsafe.json').exists())
    def test_unsafe_observation_and_exact_dates_rejected(self):
        base=load(ROOT/'examples/synthetic-submission.json')
        for mutate in ('observation','timestamp','repository','account'):
            data=copy.deepcopy(base)
            if mutate=='observation':data['observations'][0]['requirement']='SYNTHETIC_SECRET_SENTINEL'
            elif mutate=='timestamp':data['daily'][0]['timestamp']='2026-09-01T12:00:00Z'
            elif mutate=='repository':data['totals']['repository_name']='example-private'
            else:data['setup']['account']='example-person'
            with self.subTest(mutate=mutate),self.assertRaises(ValidationError):validate(data)
    def test_malformed_alternatives_fail_without_type_error(self):
        data=load(ROOT/'examples/synthetic-submission.json')
        data['observations'][0]['alternatives_considered']=[{'secret':'SYNTHETIC_SECRET_SENTINEL'}]
        with self.assertRaises(ValidationError):validate(data)
    def test_partial_line_fails(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d);(home/'sessions').mkdir();(home/'sessions/a.jsonl').write_text('{"private":"SYNTHETIC_SECRET_SENTINEL"')
            with self.assertRaises(ValidationError):aggregate(home,'2026-09-01','2026-09-02','gpt-6-astra')
if __name__=='__main__':unittest.main()
