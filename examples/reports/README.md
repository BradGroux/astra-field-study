# Full report example

[Download the complete synthetic HTML report](synthetic-report.html). Save the raw file and open it locally in a current browser; GitHub's file page shows source rather than running HTML. The file contains its data, charts, narrative, and reader runtime. It does not need a server, adjacent files, or an upload. If the enhanced reader cannot start, semantic tables keep the report readable.

The report uses only [the invented schema 1.1 ratings fixture](../synthetic-ratings-submission.json). It covers activity, token composition, reviewed observations, separate immediate/recalled rating distributions, missingness, next steps, and limitations. It is an example of report structure, not actual participant findings. It is separate from the published observational case-study explorer.

## Reproduction

`python3 tools/build_report_example.py` validates the synthetic fixture and writes the canonical `examples/reports/synthetic-report.artifact.json`. Run it from the repository root. This standard-library generator is intentionally **example-only**: its explanatory text describes the checked-in fixture, and it must not be repurposed by substituting personal data. It reads no session history or source databases. The in-memory SQLite tables contain only derived synthetic chart/table rows, with the executed SELECT queries recorded as provenance.

The HTML was packaged with the installed Data Analytics portable report renderer. It is a maintainer rendering tool, not a participant runtime dependency. With that plugin already installed, set `DATA_ANALYTICS_PLUGIN_ROOT` to its actual installation directory and run:

```sh
python3 tools/build_report_example.py
node "$DATA_ANALYTICS_PLUGIN_ROOT/skills/build-report/scripts/deliver_portable_artifact.mjs" \
  --input examples/reports/synthetic-report.artifact.json \
  --output examples/reports/synthetic-report.html
```

Do not install software just to view the checked-in HTML. Use the [README prompt](../../README.md#make-a-full-private-html-report) to request a fresh report from your own validated aggregates; do not copy the example's narrative, claims, or consent settings.

## Evidence and chart choices

- Activity uses an exact table: one represented day cannot support a trend. Missing day 2 is not synthesized as zero.
- Token bars use exclusive cached input, other input, and output components. Reasoning output remains a subset of output.
- Satisfaction and ease use separate score-distribution bars, with immediate and recalled series distinguished. Repeating the form preserves comparability without pooling dimensions or timing.
- Observation categories use a table because they are qualitative evidence, not a model-failure denominator.
- Coverage uses exact counts and question-specific denominators; unknown invitation counts stay null.
- The executive summary is followed by evidence and interpretation, next steps, further questions, and limitations. No causal comparison, cost estimate, or productivity score is justified.

The generator and embedded datasets were checked against the fixture. Portable artifact validation, packaging, and exact-payload structural verification passed. The installed-browser verification timed out, and the in-app browser disallowed the local-file URL. Desktop/mobile layout, rendered charts, source-dialog interactions, and offline browser behavior have **not** been verified for this example. No screenshot is presented as a verified preview.
