# Observational evidence format 1.0

This format publishes a reviewed case study with aggregate usage, contextual coding, and repository activity. It is **separate from submission schemas 1.0 and 1.1**. Existing collectors, submission validators, synthetic examples, and optional direct ratings remain unchanged. Do not feed an audit export into the contribution validator or treat this broader format as permission to publish a source store.

The first real case is [Study 0001: six-day Astra observation](../evidence/study-0001-v1/README.md). Its counts are not synthetic, while every fixture under `examples/` remains synthetic.

## Contract

[The schema](../schema/observational-evidence-v1.schema.json) is generated from [the closed schema definition](../tools/evidence_schema.py). Every object rejects unknown fields. Payload strings are enumerated: format/model/protocol values, generic Project and Observer labels, input-surface categories, outcome categories and a ratings-not-collected marker. Counts and duration values are bounded integers; net text-line delta can be negative. The envelope contains no free-text, paths, URLs, timestamps or original identifiers, even as hashes.

| Field | Meaning |
|---|---|
| `format`, `format_version` | `observational_evidence`, `1.0`; unrelated to submission schema version numbers. |
| `synthetic` | Whether the counts are invented. Real evidence must remain `false`. |
| `consent` | Explicit public-release review and MIT-contribution consent; required by `--ready`. |
| `model`, `study_days` | Controlled model label and relative window length. Model attribution limits belong in the accompanying methods. |
| `direct_ratings` | `not_collected` in this version. No retrospective inference or blended score. |
| `usage` | Summary, day, project, observer and day/project/observer aggregates. |
| `coded_observations` | Protocol 1.1 counts, episode/outcome counts, day/project cross-section and separate surface partition. |
| `repository_activity` | Full-window, all-author events and net diffs for identified projects, plus unresolved coverage. |

Zero-filled diff categories preserve the snapshot's path classification: documentation, dependency locks, tests, and other source/assets. They do not independently identify generated code or production code. The reader is derived from the canonical file and carries no additional private dimensions.

## Accounting checks

```sh
python3 tools/validate_evidence.py evidence/study-0001-v1/evidence.json --ready
```

The standard-library validator checks:

- Token inclusion and total relationships; completed/incomplete turn accounting.
- Additive count partitions and cross-group reconciliation.
- Distinct task and interval-union bounds without treating them as additive.
- Exclusive D/C partitions, overlap, episode outcomes and process counts.
- Unique relative-day/project/observer keys and known project coverage.
- Full-window issue/PR states, event totals, net diffs, category partitions and unresolved repositories.
- Explicit release and license consent in ready mode.

It rejects invalid JSON, duplicate keys, unknown fields, unsupported versions, out-of-range values and inconsistent accounting. Error output does not echo source values or rejected paths. Validation establishes structure and consistency, not truth, independent coding reliability, anonymity, author identity, or safe disclosure.

The schema bounds labels and arrays for this format; future requirements may need a new version. Do not silently extend the vocabulary, weaken the validator, or add narrative to a JSON object.

## Revisions and narrative

Accompany a case with a human-reviewed methods document explaining population, exclusions, model attribution, measurement units, coding, outcomes, missingness, source selection and limitations. Narrative must be authored from approved findings; it must not copy private source text, original identifiers, mappings, exact execution timestamps, or private provenance. Public methods articles and selected public replies may be linked as external context without joining generic project rows to named repositories.

A frozen case revision should use a new evidence version with a short aggregate-level change note. Keep source hashes and identity mappings private. Never revise an old result silently or represent a schema conversion as new observations.

## Neutral study identifiers

Use `evidence/study-NNNN-vV/`, such as `evidence/study-0001-v1/`, and label the package “Study 0001” rather than naming its contributor. The study number identifies a package, not a person or a globally unique participant. Do not put a person, account, employer, repository, source identifier, or identity hash in the directory name. Do not publish a private ID-to-person mapping.

Use generic observer labels in findings and package descriptions. Public source citations may retain their proper authors, and license notices must retain the required copyright attribution. Neutral naming is de-identification, not a claim of anonymity: linked publications, Git history, and public authorship can identify an already published case.

A path/label-only rename does not create new observations or require a new evidence version. Document it, preserve the frozen data bytes, and update tooling and links. Changes to measurements still require a new evidence version.

## Privacy and compatibility

Review the entire file bundle: JSON, JavaScript, download handlers, tooltips, SVG metadata, filenames, Markdown, HTML, source references, commit/PR text and vendor licensing. De-identification does not guarantee anonymity. Numeric patterns and public contributor identity remain observable.

The case-study format does not replace `tools/collect.py`, `tools/validate.py`, or `tools/sanitize.py`. Direct participant ratings still use the optional submission 1.1 protocol, where they remain separate from usage and coding. Supporting real ratings in a future case-study format requires its own explicit versioned contract.
