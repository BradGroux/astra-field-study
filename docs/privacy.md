# Privacy and disclosure boundaries

The public submission schema accepts only numeric counts, study-relative day numbers, booleans, explicit nulls and enumerated categories. There are no free-text, URL, repository-name, path or identity fields. The collector creates this output from an explicit allowlist; it does not dump a source object and remove a few keys afterward. Original identifiers are used transiently for local deduplication and never leave the aggregate process.

The validator rejects unknown fields at every object level, unknown categories, invalid accounting, duplicate JSON keys and unsupported schema versions. Errors do not echo rejected values or source records. `sanitize.py` is a canonicalization step, not a regex redactor. Never feed it raw history expecting it to remove secrets.

These controls **do not guarantee anonymity or safe disclosure**. De-identified payloads are not anonymous submissions: GitHub pull requests expose the contributor account. Counts, relative-day patterns, contribution timing and public Git identity can reveal activity. Deliberately encoding a secret in numeric values cannot be prevented by a schema. You must review the complete JSON, filename, Git diff, commit metadata and PR text, and obtain necessary permissions before public sharing. A valid schema does not verify the truth of an observation.

Never submit:

- Credentials, tokens, keys, prompts, conversations, tool output or private task descriptions.
- Any repository names (public or private), local paths, aliases with a private mapping, or links into private work.
- Original response, turn, task, session or message identifiers, including hashed versions.
- Codex SQLite files, session JSONL, archives, screenshots or raw source inventories.

Draft collection writes a new file outside the checkout and source store. It does not write a private mapping or raw sidecar. Keep drafts local until reviewed. Do not attach private files when reporting a bug; reproduce with synthetic records. No collector, validator or sanitizer in this kit contains upload code. Publishing remains a separate action you control.


Optional direct ratings in schema `1.1` add only bounded integers, null answers, timing categories and coverage counts. They contain no original identifiers, timestamps, project/machine names or narrative. Nulls disclose missingness; they are never converted into neutral or satisfied responses. The usage collector leaves this layer absent. Adding real ratings requires the same full-file review and explicit release/license consent. Do not include local rating-to-task mappings or any hashes of source identities.

## Separately reviewed observational cases

Real case-study aggregates may live in `evidence/` under the separate [observational evidence format](observational-evidence-format.md). This does not widen the participant submission schemas or authorize raw-history exports. The same privacy boundary applies to JSON and every accompanying reader asset, download, figure, filename and narrative. Case data must be explicitly reviewed for public release and MIT contribution; original identities, source hashes, mappings, private text/URLs and public joins to named projects remain excluded. Numeric consistency is not an anonymity guarantee.
