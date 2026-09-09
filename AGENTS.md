# Repository instructions

## Purpose and interpretation

Astra Field Study is a community kit for collecting local coding-agent activity and submitting reviewed, de-identified aggregate findings. Preserve the distinction between measured descriptive activity, coded observations, direct participant ratings, and untested causal hypotheses. Invite contrary evidence and successful adherence examples. Never claim that efficiency itself is cheating, that token volume measures useful work or cost, or that these observational counts establish a model failure rate or matched model comparison.

## Read before working

- `README.md`: project entry point, published resources, and supported local commands.
- `CONTRIBUTING.md` and `submissions/README.md`: participant submission and maintainer review workflow.
- `docs/privacy.md`: public disclosure boundary for all data, docs, assets, and PR content.
- `docs/methodology.md`: collector support, metrics, accounting, and coverage limits.
- `docs/local-collection-prompt.md`: local-only collection task and stopping point.
- `docs/local-results.md`: private terminal summaries and validated JSON/CSV export examples.
- `docs/self-reported-ratings.md`: optional direct ratings and missingness rules.
- `docs/observational-evidence-format.md`: separate real case-study format.
- `docs/reader-design.md`: reader/figure generation and visual verification.

## Repository ownership

- `tools/`: standard-library Python collector, validators, canonicalizer, and reader/figure tools.
- `schema/`: participant formats 1.0/1.1 and the separate observational evidence format.
- `examples/` and `tests/`: synthetic data and fixtures only; never copy real audit evidence here.
- `submissions/`: manually reviewed, consented participant aggregate JSON only.
- `evidence/`: separately reviewed, versioned real observational packages. These are not normal participant submissions.
- `CHANGELOG.md`: package changes. A package version does not silently change data schema or frozen evidence versions.

The published study is https://go.sstb.ai/astra-study, the companion blog is https://go.sstb.ai/astra-blog, and the repository short link is https://go.sstb.ai/astra-repo. Use these short links for these resources and verify destinations before changing publication claims. Editorial source and social drafts belong in `DigitalMeld/digitalmeld.io`, under `docs/drafts/2026-09-09-astra-field-study`, not here. Do not describe an unpublished social draft as published or link to a nonexistent short URL.

## Helping someone submit findings

The supported route is a reviewed JSON contribution in `submissions/`, submitted by pull request from the contributor's fork to `main`. There is no hosted form or automatic upload. Discussions accept safely described experiences and questions, including contrary results; they are not validated dataset entries. Issues for parser or schema changes must use synthetic examples.

1. Read the contribution and privacy guides before collecting. Use the contributor's specified model/client/effort and a bounded UTC window; leave uncertain categories unknown. Keep the new draft outside this checkout and the source store.
2. Use only the supported collector. Do not invent fallback extraction, inspect SQLite, alter source history, or estimate unsupported/incomplete records. Explain limitations without printing raw records or private identifiers.
3. Leave both consent fields false. The contributor must review the complete JSON and explicitly decide public release and licensing. Never infer consent from a request to collect or validate, and never set consent on their behalf.
4. Observations require reviewed local evidence and controlled categories, not inference from usage volume. Direct ratings require actual participant answers; never reconstruct them from conversations. Keep missing values and immediate/recalled timing separate.
5. After the contributor's separate submission decision and completed consent, follow `CONTRIBUTING.md` to validate, canonicalize to a new neutral filename, review the exact diff, and prepare the PR. Do not overwrite submissions or count overlapping exports as independent findings.
6. Stop at the authorized stage. Collection, validation, a saved draft, PR submission, maintainer acceptance, website deployment, and social publication are distinct outcomes. Never publish from a local-only request.

## Private viewing and exports

For a request to inspect or export personal results, follow `docs/local-results.md`. Validate participant JSON without `--ready`; public consent is not needed for private viewing. Keep consent unchanged and outputs outside the checkout in a new directory. Do not use the consent-required sanitizer merely to view data. Export only validated aggregates, never raw history, and do not upload results or open them in a hosted service without separate authorization.

Explain window versus daily rows, overlapping distinct counts, token subsets, missing days, and optional rating timing/denominators. The existing interactive reader serves the frozen observational case and is not a participant JSON importer. Do not overwrite or relabel the case to display someone else's data. CSV is a viewing derivative; submissions remain validated JSON. Verify documentation export examples with synthetic inputs, including false-consent data and refusal to overwrite existing outputs.

## Privacy and maintainer review

Keep private history out of this public repository. Do not include raw logs, prompts, tool output, SQLite, credentials, screenshots, any repository names in payloads, private paths, mappings, or original identifiers, even as hashes. The boundary applies to filenames, commits, PR descriptions, attachments, figures, and reader downloads as well as JSON. `sanitize.py` canonicalizes allowlisted JSON; it does not redact raw history.

Review each submission's exact diff, format version, numeric accounting, synthetic flag, both consent fields, rights, coverage, and overlap limitations. Real data must retain `synthetic: false`. Passing validation does not prove safe disclosure, anonymity, or truth. GitHub identities and commit metadata remain public. If sensitive content appears, stop further sharing; do not quote it into an issue or review comment. Escalate privately to the maintainer rather than promising that later removal erases public copies.

Frozen observational evidence corrections require a new evidence version and an aggregate-level change note. Do not silently revise measurements or private provenance. Schema changes require an explicit version decision, compatibility review, synthetic fixtures, and local tests.

## Local verification and publication

Use Python 3.10+ and the standard library. Run applicable checks from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate.py examples/synthetic-submission.json --ready --preview
python3 tools/validate.py examples/synthetic-ratings-submission.json --ready --preview
python3 tools/validate_evidence.py evidence/brad-groux-six-days-v1/evidence.json --ready
git diff --check
```

For a participant submission, also run `tools/validate.py` with `--ready` against the exact new JSON. Read the entire file and diff; a terminal preview is insufficient. For ordinary documentation edits, check affected links and claims. For figure or reader changes, follow `docs/reader-design.md` and inspect rendered output; a build alone is not visual verification.

Never add, enable, trigger, rerun, or require GitHub Actions or connected third-party CI. Inspect applicable workflow files, repository controls, hooks, and connected checks before pushing, creating a PR, or merging. No production dependencies without explicit approval. No automatic uploads or consent on a contributor's behalf. Preserve unrelated local work and report only outcomes supported by verification and destination readback.

## License

Original code, docs, and contributed datasets use MIT. Contributors retain their rights and must have permission to release their work. Preserve copyright and permission notices. Linked third-party content keeps its own terms; do not relicense it implicitly.
