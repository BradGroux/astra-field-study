# Export and view your own results locally

You can inspect your aggregate without submitting it or consenting to public release. Keep both consent fields false while working privately. Run these commands from the Astra Field Study checkout with Python 3.10 or later; no additional Python packages are needed.

Start with the [local collection instructions](local-collection-prompt.md). The examples below assume the collector wrote `/tmp/astra-draft.json`. Replace that path with your own local aggregate. Use only aggregate JSON accepted by the participant validator, never raw session history or SQLite.

## Read a terminal summary

```sh
python3 tools/validate.py /tmp/astra-draft.json --preview
```

This validates the full aggregate and prints a JSON summary of setup, window, totals, observation count, and consent. If actual optional ratings are present, it also reports satisfaction and ease distributions and coverage separately by timing group. It does not display every daily row or observation; review the complete JSON in your text editor too.

Do not add `--ready` for private viewing: that flag requires public-release and licensing consent. Likewise, `sanitize.py` is for a consented submission, not a prerequisite for viewing your own data.

To try the summary before collecting anything:

```sh
python3 tools/validate.py examples/synthetic-submission.json --preview
python3 tools/validate.py examples/synthetic-ratings-submission.json --preview
```

These files are invented demonstrations, not your results. Their consent values do not give consent for your own records.

## Export JSON and spreadsheet-friendly CSV files

The following copy-and-paste example validates the input first, then creates a **new** output directory outside the checkout. Replace both paths as needed. Choose a fresh output directory each time: an existing directory is refused, so earlier exports are preserved. `/tmp` is temporary; choose a private local directory outside the repository for long-term retention.

```sh
python3 - /tmp/astra-draft.json /tmp/astra-view-001 <<'PY'
import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path('tools').resolve()))
from validate import ValidationError, load, preview, validate

try:
    data = validate(load(Path(sys.argv[1])))
except (ValidationError, OSError, RecursionError):
    raise SystemExit('Invalid aggregate; nothing exported. No input content displayed.')

out = Path(sys.argv[2])
try:
    out.mkdir(exist_ok=False)
except OSError:
    raise SystemExit('Choose a new writable output directory; nothing exported.')

(out / 'aggregate.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
(out / 'summary.json').write_text(preview(data) + '\n', encoding='utf-8')

counts = ['responses', 'turns_with_responses', 'tasks_with_responses',
          'native_user_message_items', 'repository_contexts_with_responses']
tokens = ['input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
          'output_tokens', 'reasoning_output_tokens', 'total_tokens']
with (out / 'usage.csv').open('x', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=['scope', 'day_index'] + counts + tokens)
    writer.writeheader()
    for scope, row in [('window', data['totals'])] + [('day', d) for d in data['daily']]:
        writer.writerow({'scope': scope, 'day_index': row.get('day_index', ''),
                         **{key: row[key] for key in counts},
                         **{key: row['tokens'][key] for key in tokens}})

fields = ['requirement', 'behavior', 'delegation', 'instruction_access',
          'result', 'evidence_basis', 'alternatives_considered']
with (out / 'observations.csv').open('x', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for observation in data['observations']:
        writer.writerow({**observation,
                         'alternatives_considered': '; '.join(observation['alternatives_considered'])})

print('Created aggregate.json, summary.json, usage.csv, and observations.csv. Nothing uploaded.')
PY
```

The destination's parent directory must already exist. The script reads only the aggregate you supply and writes the four named files. It does not collect again, change the source file, change consent, or contact a server. Validation rejects unrecognized free text before any export, so the CSV uses only controlled categories and numeric counts. A valid file can still reveal work patterns: local viewing is not an anonymity guarantee.

### Open the outputs

- Open `aggregate.json` in a text editor for the complete data, including diagnostics, observations, and any actual ratings.
- Open `summary.json` in a text editor for a compact summary and any rating distributions. Unknown values remain JSON `null`.
- Open `usage.csv` in a local spreadsheet application for sorting or charting. Filter `scope` to `day` for daily charts; use the `window` row for whole-window totals. **Do not sum the window row together with daily rows.**
- Open `observations.csv` for the controlled observation categories. An empty observation list produces only the column headings, not invented findings.

Use a local editor or spreadsheet if you want to keep this private. Importing these files into a hosted spreadsheet or sharing service is a separate upload decision. These CSV derivatives are for your own viewing; participant submissions still use the validated JSON format.

### Worked synthetic example

To run the export demonstration, replace `/tmp/astra-draft.json` in the command with `examples/synthetic-submission.json` and choose a new directory such as `/tmp/astra-example-view-001`.

Its `usage.csv` is:

```csv
scope,day_index,responses,turns_with_responses,tasks_with_responses,native_user_message_items,repository_contexts_with_responses,input_tokens,cached_input_tokens,cache_write_input_tokens,output_tokens,reasoning_output_tokens,total_tokens
window,,1,1,1,1,1,100,80,0,10,4,110
day,1,1,1,1,1,1,100,80,0,10,4,110
```

The requested window is two days, but only day 1 has a retained row. Do not manufacture a day 2 zero or interpret absent rows as zero account activity. Daily distinct turns, tasks, and repository contexts can overlap across days; use the window totals rather than summing those daily distinct counts.

The 80 cached input tokens are included in the 100 input tokens; the 4 reasoning output tokens are included in the 10 output tokens. Do not add these subsets again. These numbers describe recorded activity, not cost or useful work.

For the optional ratings demonstration, use `examples/synthetic-ratings-submission.json`. `summary.json` includes `self_report_summary` with separate timing groups, answer distributions, missingness, coverage, and CSAT. `aggregate.json` retains the individual supplied ratings. No ratings are inferred or blended into an overall quality score. See the [rating interpretation guide](self-reported-ratings.md#read-the-results).

## About the interactive study explorer

`tools/preview_reader.py` serves Brad's published observational case. It does **not** load your participant submission, and `tools/build_evidence_reader.py` expects the separate observational evidence format. Do not replace the frozen case or relabel your participant JSON to make it fit. Use the JSON/CSV workflow above for your own results. A general participant explorer would be a separate feature.

If you later decide to share findings, follow [CONTRIBUTING.md](../CONTRIBUTING.md) for full review, consent, validation, and a pull request. Exporting or viewing these files does not submit them.
