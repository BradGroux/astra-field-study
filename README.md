# Astra Field Study

A community kit for studying how coding agents follow instructions in everyday work. The starting point is simple: **this is what I currently think, but I want to know more.** Bring successful experiences, failures, and counterexamples.

Two entirely untested hypotheses motivate the project:

1. Efforts to finish efficiently may sometimes override the intended process or its constraints.
2. Delegation may lose SOP instructions or other requirements between the main agent and its subagents.

These are hypotheses formed from roughly four or five days of personal experience, not conclusions about a model's internal objectives. Efficiency can be useful and fully compliant. It is not itself cheating. Shared bad strategies, missing context, tool failures and unclear instructions are different possible explanations.

Usage counts describe activity. They do not establish SOP adherence, model authorship, productivity gains or either proposed cause. This is an observational project with voluntary, self-selected contributions, no randomized comparison and no account-wide completeness guarantee. The initial repository contains **synthetic data only**.

## Try the kit

Python 3.10 or later; standard library only. Run from this checkout:

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate.py examples/synthetic-submission.json --ready --preview
```

To collect your own retained records, first read the [local collection prompt](docs/local-collection-prompt.md) and [privacy rules](docs/privacy.md). Choose your own UTC date range and a **new draft file outside this checkout and your Codex store**. Example dates below are illustrative:

```sh
python3 tools/collect.py --start 2026-09-01 --end 2026-09-02 --model gpt-6-astra --client codex_desktop --out /tmp/astra-draft.json
python3 tools/validate.py /tmp/astra-draft.json --preview
```

The collector reads only local JSONL under `~/.codex/sessions` and `~/.codex/archived_sessions` by default. Use `--home` for another local store. It makes no network requests, never reads SQLite, never modifies source history, and uploads nothing. It exports counts, study-relative day numbers and controlled categories. It does **not** export repository names, paths, prompts, tool output or original record identifiers.

Only the evidenced native `token_usage_record` format with matching `turn_context` is supported. Older clients that only retain cumulative `token_count` snapshots cannot be measured by this collector. Unsupported, incomplete or conflicting evidence is rejected rather than estimated. See [metric definitions and format limits](docs/methodology.md).

## Optional direct ratings

Keep measured activity, coded observations, and participant ratings separate. The optional [task satisfaction and ease protocol](docs/self-reported-ratings.md) adds actual 1–5 satisfaction and 1–7 SEQ answers, with explicit missingness and invitation coverage. Immediate responses and later recollection are reported separately. The collector never infers ratings, and there is no blended quality index.

```sh
python3 tools/validate.py examples/synthetic-ratings-submission.json --ready --preview
```

[Schema 1.1](schema/submission-v1.1.schema.json) adds this optional layer; existing 1.0 submissions remain valid and unchanged. Both examples contain invented data only.

## Participate

Read [CONTRIBUTING.md](CONTRIBUTING.md). Submit a reviewed aggregate JSON through a pull request, or use [Discussions](https://github.com/BradGroux/astra-field-study/discussions) for questions and contradictory experiences. Successful adherence examples are as useful as deviations. If a useful observation does not fit the controlled categories, propose a schema change with a synthetic example; do not add private narrative to a submission.

The versioned [schema](schema/submission-v1.schema.json), [synthetic example](examples/synthetic-submission.json) and local checks make contributions inspectable. De-identified payloads are not anonymous participation: GitHub pull requests expose the contributor account and commit metadata, and activity patterns can identify people. These checks do not guarantee anonymity or remove the need to review disclosure and permissions. Never upload Codex session history or databases, even when asking for troubleshooting help.

All validation runs locally. This repository has no GitHub Actions, connected CI, or CI merge requirement.

## License

Original project code, documentation and contributed datasets are licensed under [MIT](LICENSE), copyright Brad Groux 2026 for the initial project. Contributors retain their rights and license their original contributions under MIT. Reuse requires preserving applicable copyright and permission notices; it does not require promotional credit or a link. Linked third-party papers, tweets, articles and vendor documentation retain their own terms and are not relicensed by this repository.
