# Contributing

Counterexamples are welcome. Do not select only failures: include successful adherence when available and say what else could explain the observed result. Neither a large token count nor an agent's own explanation establishes a causal mechanism.

## Choose how to contribute

- **Submit findings:** open a pull request adding one reviewed aggregate JSON file under `submissions/`. Follow the collection, consent, and validation steps below. Successful adherence, mixed outcomes, and inconclusive observations are welcome alongside failures.
- **Discuss an experience or ask a question:** use [GitHub Discussions](https://github.com/BradGroux/astra-field-study/discussions). You do not need to upload data. Keep descriptions safe for public disclosure; do not attach raw history or private evidence. Discussion posts are not validated dataset submissions.
- **Report a tool problem or suggest a schema change:** open a [GitHub issue](https://github.com/BradGroux/astra-field-study/issues) with a minimal synthetic example. Unsupported data formats should be reported rather than forced into the schema.

There is no hosted submission form or automatic upload. A local draft is not a submission; publishing a reviewed contribution is a separate decision.

## Prepare locally

You can first [view and export results privately](docs/local-results.md), including JSON and CSV examples, without agreeing to publication.

1. Run the collector as described in the README, keeping its draft outside this checkout. Use one store and one non-overlapping collection window per contribution. Aggregate exports cannot deduplicate records across machines or identify overlap; do not sum multiple exports as unique usage.
2. Read the **entire** draft JSON, including relative day numbers, categories, counts and observations. The terminal preview is a summary, not the full review. Consider whether even an aggregate reveals private work patterns. Do not collect someone else's records without their permission.
3. Optionally add `observations` using only the schema's controlled vocabulary. Summarize the requirement by category, then separately label observed behavior, instruction access, delegation, result, evidence basis and alternative explanations. Review the relevant local evidence yourself; do not copy it into the JSON or PR. Include a `followed_requirement` example when you have one. Use `inconclusive` or `recollection_only` when appropriate. See the synthetic example for structure, not real findings.
4. Optionally add actual participant ratings using the [satisfaction and ease protocol](docs/self-reported-ratings.md) and schema `1.1`. Keep all ratings from one participant, separate immediate/recalled/unknown timing, use `null` for skipped answers and unknown invitation/eligibility counts, and never reconstruct ratings from transcripts. Existing `1.0` files remain valid without ratings. Invite ordinary work, successful adherence and counterexamples equally. Review the full rating payload and its coverage preview before consent.
5. Verify the manually selected client and reasoning-effort categories. Leave `unknown` when uncertain. Do not infer server-resolved model identity from the UI or token counters.
6. Only if you have reviewed public disclosure and hold the necessary rights/permissions, change both `consent` booleans to `true`. Real data must retain `synthetic: false`. The collector never supplies consent on your behalf.
7. Choose a new neutral filename such as `submissions/entry-0001.json`, without an employer, project, person, task ID or date that you do not intend to disclose. Fork/branch locally, then run:

```sh
python3 tools/validate.py /tmp/astra-draft.json --ready --preview
python3 tools/sanitize.py /tmp/astra-draft.json --out submissions/entry-0001.json
python3 tools/validate.py submissions/entry-0001.json --ready
python3 -m unittest discover -s tests -v
git diff --check
git diff --no-index /dev/null submissions/entry-0001.json
```

The last command normally exits 1 because it displays a new file; review every field. `sanitize.py` validates and canonicalizes an already allowlisted aggregate. It **does not scrub raw logs** and refuses unexpected fields. It will not overwrite an existing file.

## Open a pull request

1. Fork [Astra Field Study](https://go.sstb.ai/astra-repo) to your own GitHub account and create a contribution branch in your local fork. Follow your own applicable automation policy before publishing to a fork.
2. Add only the new `submissions/` JSON that passed the steps above. Check that the neutral filename is unused; do not overwrite another contribution or include the original local draft.
3. Review the staged diff and your public commit identity, commit the file, and push the contribution branch to your fork.
4. Open a pull request from that branch to `BradGroux/astra-field-study` on `main`. Use a neutral title such as “Add reviewed aggregate contribution.”
5. Include the information below, then wait for maintainer review. A submitted PR is not an accepted finding or endorsement of a causal explanation.

Suggested PR body (complete these statements only when true):

```text
Contribution type: real reviewed aggregate / synthetic example
Schema version: 1.0 / 1.1
Local verification: commands run and results
Disclosure review: I reviewed the complete JSON, diff, filename, and public metadata.
Rights and consent: I have permission to publish this contribution under MIT.
Coverage and overlap: non-sensitive limitations and any overlap with an earlier submission
```

For corrections to an accepted contribution, identify the earlier public submission and explain the aggregate-level correction in a new PR. Do not upload overlapping records as a new independent contribution. Never add private provenance to explain the correction.

Submit only the intended reviewed JSON or scoped code/docs changes. State whether data is synthetic, list the local checks you ran, and confirm you have the rights to release your contribution under MIT. Explain collection overlap or limitations using non-sensitive descriptions. Do not paste raw logs, original identifiers, prompts, credentials, private repository names or local paths into the PR, its title, commits or attachments. Git commit metadata and your GitHub account are public too. This is a de-identified data payload, not an anonymous submission. Do not name any repository in the payload, whether public or private; no naming exceptions apply.

By submitting, you agree to license your original contribution under the repository's MIT license. You must have the rights and permissions to share it publicly. Contributors retain their own copyright; downstream users must preserve applicable copyright and permission notices. Do not submit third-party material you cannot license. This project makes no legal guarantee about your particular data or situation.

Maintainers review the exact diff, schema, accounting, synthetic flag, consent and collection limitations before accepting a submission. A passed validator is not a finding that disclosure is safe or that a claimed observation is true. If anything sensitive appears, stop sharing it; removing a file later cannot guarantee removal from public copies.

## Questions and schema improvements

Use Discussions for public feedback, including experiences that contradict the hypotheses. A controlled vocabulary deliberately limits detail. Suggest additions with synthetic examples when it cannot capture your case safely. Schema changes need a version decision and local tests. Never upload session JSONL or SQLite to demonstrate a parser failure; construct a minimal synthetic fixture instead.

No GitHub Actions or connected CI may be added, triggered or required. Run all checks locally. Do not add production dependencies without approval.

## Larger observational evidence packages

The [versioned observational format](docs/observational-evidence-format.md) is separate from normal participant submissions. Do not place an audit export into `examples/` or bypass the narrower contribution validator. Propose format changes with synthetic fixtures, retain all privacy boundaries, and obtain explicit release/license review before adding real case aggregates. No direct ratings may be inferred from source text.
