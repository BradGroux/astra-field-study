#!/usr/bin/env python3
"""Build the canonical synthetic report artifact; reads no personal records."""
import json
import hashlib
import sqlite3
from pathlib import Path
from validate import validate, self_report_summary

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'examples/synthetic-ratings-submission.json'


def build():
    raw = (ROOT / SOURCE).read_bytes()
    if hashlib.sha256(raw).hexdigest() != '865cf1fb09dd2155425e311f68e2ced00c63d51a08a947ade0bebf74feeca6e9':
        raise ValueError('Fixture changed: review the report narrative before rebuilding.')
    data = validate(json.loads(raw))
    if data['synthetic'] is not True:
        raise ValueError('This example generator accepts synthetic data only.')
    tokens = data['totals']['tokens']
    ratings = self_report_summary(data['self_reports'])['groups']
    title = 'A personal field-study report — synthetic example'
    stamp = '2026-09-09T00:00:00Z'
    source = {'id': 'fixture', 'label': 'Invented participant example, schema 1.1', 'path': SOURCE}
    datasets = {
        'activity': [{'measure': label, 'count': data['totals'][key]} for key, label in [
            ('responses', 'Responses'), ('turns_with_responses', 'Turns with responses'),
            ('tasks_with_responses', 'Tasks with responses'),
            ('repository_contexts_with_responses', 'Repository contexts')]],
        'tokens': [{'component': 'Cached input', 'tokens': tokens['cached_input_tokens']},
                   {'component': 'Other input', 'tokens': tokens['input_tokens'] - tokens['cached_input_tokens']},
                   {'component': 'Output', 'tokens': tokens['output_tokens']}],
        'observations': [{'requirement': o['requirement'].replace('_', ' '),
                          'behavior': o['behavior'].replace('_', ' '),
                          'result': o['result'].replace('_', ' '),
                          'instruction_access': o['instruction_access'].replace('_', ' ')} for o in data['observations']],
        'satisfaction': [{'score': str(score), 'answers': count,
                          'timing': 'Immediate' if g['timing'] == 'immediately_after_task' else 'Recalled'}
                         for g in ratings for score, count in enumerate(g['satisfaction']['rating_counts_low_to_high'], 1)],
        'ease': [{'score': str(score), 'answers': count,
                 'timing': 'Immediate' if g['timing'] == 'immediately_after_task' else 'Recalled'}
                for g in ratings for score, count in enumerate(g['task_ease']['rating_counts_low_to_high'], 1)],
        'coverage': [{'timing': 'Immediate' if g['timing'] == 'immediately_after_task' else 'Recalled',
                      'measure': label, 'eligible': g['eligible_task_attempts'],
                      'invited': g['invited_task_attempts'], 'recorded': g['recorded_task_attempts'],
                      'answered': g[field]['answered'], 'unanswered': g[field]['recorded_unanswered'],
                      'coverage': g[field]['response_coverage_percent'] / 100 if g[field]['response_coverage_percent'] is not None else None}
                     for g in ratings for field, label in [('satisfaction', 'Satisfaction'), ('task_ease', 'Task ease')]],
    }
    # Use real, reproducible SQL over in-memory synthetic derived tables for
    # the portable reader's SQL provenance contract. No source store is opened.
    sources = [source]
    with sqlite3.connect(':memory:') as db:
        for name, rows in datasets.items():
            fields = list(rows[0])
            db.execute(f'CREATE TABLE {name} (' + ', '.join(fields) + ')')
            db.executemany(f'INSERT INTO {name} VALUES (' + ', '.join('?' for _ in fields) + ')',
                           [[row[field] for field in fields] for row in rows])
            sql = f'SELECT * FROM {name}'
            datasets[name] = [dict(zip(fields, row)) for row in db.execute(sql)]
            sources.append({'id': name + '-source', 'label': 'Synthetic example: ' + name,
                            'path': SOURCE, 'query': {'engine': 'SQLite in memory', 'sql': sql,
                            'tables_used': [name], 'description':
                            'Validated synthetic JSON transformed by tools/build_report_example.py, '
                            'then selected from an in-memory derived table. No personal database is read.'}})
    charts = []
    def chart(identifier, title, dataset, x, y, xlabel, ylabel, color=None):
        encoding = {'x': {'field': x, 'type': 'ordinal', 'label': xlabel},
                    'y': {'field': y, 'type': 'quantitative', 'label': ylabel, 'format': 'number'}}
        if color:
            encoding['color'] = {'field': color, 'type': 'nominal', 'label': 'Rating timing'}
        charts.append({'id': identifier, 'title': title, 'type': 'bar', 'dataset': dataset,
                       'sourceId': dataset + '-source', 'encodings': encoding,
                       'yAxisTitle': ylabel, 'valueFormat': 'number', 'layout': 'full'})
    chart('tokens', 'Token composition', 'tokens', 'component', 'tokens', 'Exclusive component', 'Tokens')
    chart('satisfaction', 'Satisfaction answers by score', 'satisfaction', 'score', 'answers', 'Score · 1–5', 'Answers', 'timing')
    chart('ease', 'Task-ease answers by score', 'ease', 'score', 'answers', 'Score · 1–7', 'Answers', 'timing')
    tables = []
    def table(identifier, title, columns):
        tables.append({'id': identifier, 'title': title, 'dataset': identifier, 'sourceId': identifier + '-source',
                       'columns': [{'field': field, 'label': label, **({'format': fmt} if fmt else {'type': 'text'})}
                                   for field, label, fmt in columns]})
    table('activity', 'Recorded activity across the requested window', [('measure', 'Measure', None), ('count', 'Count', 'number')])
    table('observations', 'Two reviewed observation examples', [('requirement', 'Requirement', None), ('behavior', 'Behavior', None), ('instruction_access', 'Instruction access', None), ('result', 'Outcome', None)])
    table('coverage', 'Rating coverage by timing and question', [('timing', 'Timing', None), ('measure', 'Question', None), ('eligible', 'Eligible', 'number'), ('invited', 'Invited', 'number'), ('recorded', 'Recorded', 'number'), ('answered', 'Answered', 'number'), ('unanswered', 'Recorded blank', 'number'), ('coverage', 'Answered / invited', 'percent')])
    blocks = []
    def prose(identifier, body, sourced=True):
        blocks.append({'id': identifier, 'type': 'markdown', 'body': body, **({'sourceId': 'fixture'} if sourced else {})})
    def visual(identifier, kind):
        blocks.append({'id': identifier + '-block', 'type': kind, kind + 'Id': identifier, 'layout': 'full'})
    prose('title', '# ' + title, False)
    prose('summary', '''## Executive Summary

**This is an invented worked example, not a participant finding.** It demonstrates what a complete private report can explain from validated aggregates: activity, reviewed observations, and separately collected ratings.

- **Activity is measurable; effectiveness is not established.** The fixture records one response and 110 tokens across a two-day requested window, with only day 1 represented.
- **The observation examples point in different directions.** One requirement was followed successfully; another was lost after a handoff and the deviation was corrected. These examples do not supply a failure-rate denominator.
- **The ratings are sparse and unevenly covered.** Immediate satisfaction has three answers, two of them favorable. Task ease has two immediate answers. A separate recalled answer stays separate.

Use this report to identify what needs closer review, not to rank models or infer productivity.''')
    prose('activity-context', '''## One recorded response cannot establish a trend

The activity layer contains **one response, one response-bearing turn, one task, and one repository context**. These are different units describing the same recorded activity, not four independent results. Window-level distinct counts must not be summed with daily counts.

Only day 1 has a row in a requested two-day window. Day 2 is unrepresented; it is not plotted as zero. No trend or day-over-day comparison is supported. Confirm retained-record coverage before interpreting low volume.''')
    visual('activity', 'table')
    prose('token-context', '''## Cached input accounts for most of the recorded tokens

Of **100 input tokens, 80 are cached**: 80% of the input denominator. Another 20 input tokens and 10 output tokens complete the 110-token total. The bars use mutually exclusive components so they can be added safely.

Four reasoning tokens are already included in the 10 output tokens. Cache-write input is recorded as zero. Token counts describe recorded processing volume; they do not establish cost, work quality, or time saved.''')
    visual('tokens', 'chart')
    prose('observation-context', '''## The observations show both adherence and a corrected deviation

The two reviewed examples record a successful local-check requirement and a documented-step requirement lost after delegation. In the second example, instructions were absent from the handoff and the deviation was corrected. That pattern makes context transfer worth inspecting; it does not establish an internal motive or a causal model defect.

These coded observations are a separate evidence layer. They are not linked one-to-one to the single usage response, and selected observations are not a sample of every opportunity to comply. A ratio such as “one of two observations” would describe this selection only, not an overall failure rate.''')
    visual('observations', 'table')
    prose('satisfaction-context', '''## Immediate satisfaction is mixed, with only three answers

On the **1–5 satisfaction scale**, the immediate answers are 2, 4, and 5. Two of three answered ratings are favorable (4–5), or **66.7%**. Only three of five invited attempts answered satisfaction, so invitation coverage is **60%**; three of eight eligible attempts answered, or **37.5%**.

The chart shows answer counts at every score. The separate recalled rating is 1. It is displayed as a different series and is not pooled into the immediate result. These few invented answers illustrate reporting, not a stable satisfaction estimate.''')
    visual('satisfaction', 'chart')
    prose('ease-context', '''## Task ease is split between a difficult and an easy attempt

On the **1–7 task-ease scale**, where higher is easier, the two immediate answers are 2 and 6. Showing their distribution preserves the contrast that an average would conceal. The separate recalled answer is 3.

Only two of five invited attempts answered task ease (**40%**); two of eight eligible attempts answered (**25%**). Do not combine ease with satisfaction into a quality score, or treat a blank response as a low score.''')
    visual('ease', 'chart')
    prose('coverage-context', '''## Missing answers change how much the ratings can tell us

Four immediate task-attempt entries were recorded from five invitations and eight eligible attempts. Of those entries, one lacks satisfaction and two lack ease; one entry has neither answer. The fifth invitation has no recorded entry. “Recorded blank” therefore differs from all invited attempts without an answer.

The recalled group contains one entry, with unknown eligible and invited counts. Missing values in the table mean **unknown**, not zero. Rating attempts need not match response-bearing tasks in the usage layer; the fixture does not provide a linkage or establish that the cohorts coincide.''')
    visual('coverage', 'table')
    prose('next-steps', '''## Next steps for a real personal report

1. **Check the collection window and retained format.** Establish which days and clients are represented before comparing activity.
2. **Review both successful and unsuccessful requirements.** Keep observations grounded in local evidence and record plausible alternatives, especially handoff context and instruction clarity.
3. **Collect ratings consistently.** Invite answers immediately after eligible attempts, track skipped invitations and missing answers, and preserve recalled responses as a separate group.
4. **Keep the report private until separately reviewed for release.** Private validation and HTML viewing need no public consent. Publication is a separate decision.

A larger, consistently observed set could support better descriptive comparisons. A causal claim would still need a suitable study design.''', False)
    prose('questions', '''## Questions this report cannot answer

Did the absent daily row reflect incomplete retention or no matching activity? Were the reviewed observations representative? Did unanswered rating invitations differ from answered ones? Would another model behave differently on the same tasks under the same conditions?

The aggregate alone cannot resolve these questions. No model comparison, cost estimate, causal conclusion, or productivity score is reported.''', False)
    prose('limits', '''## Scope and limitations

All values are synthetic and come from one checked-in example. The model label is GPT-6 Astra; client and reasoning effort are unknown. The observer scope is one local store. One counter snapshot was ignored and no duplicate response records were reported.

The original fixture contains example-only consent values. They are not a template for anyone’s release decision. This HTML contains aggregate example data only and requires no upload or hosted service. In a real report, describe only supplied evidence and actual participant answers.''')
    return {'surface': 'report', 'manifest': {'version': 1, 'surface': 'report', 'title': title,
            'description': 'A complete private-report example using invented, validated participant aggregates.',
            'generatedAt': stamp, 'cards': [], 'charts': charts, 'tables': tables,
            'sources': sources, 'blocks': blocks},
            'snapshot': {'version': 1, 'generatedAt': stamp, 'status': 'fixture', 'datasets': datasets},
            'sources': sources}


if __name__ == '__main__':
    target = ROOT / 'examples/reports/synthetic-report.artifact.json'
    target.write_text(json.dumps(build(), indent=2) + '\n')
    print(target.relative_to(ROOT))
