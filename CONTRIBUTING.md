# Contributing

Counterexamples are welcome. Do not select only failures: include successful adherence when available and say what else could explain the observed result. Neither a large token count nor an agent's own explanation establishes a causal mechanism.

## Prepare locally

1. Run the collector as described in the README, keeping its draft outside this checkout. Use one store and one non-overlapping collection window per contribution. Aggregate exports cannot deduplicate records across machines or identify overlap; do not sum multiple exports as unique usage.
2. Read the **entire** draft JSON, including relative day numbers, categories, counts and observations. The terminal preview is a summary, not the full review. Consider whether even an aggregate reveals private work patterns. Do not collect someone else's records without their permission.
3. Optionally add `observations` using only the schema's controlled vocabulary. Summarize the requirement by category, then separately label observed behavior, instruction access, delegation, result, evidence basis and alternative explanations. Review the relevant local evidence yourself; do not copy it into the JSON or PR. Include a `followed_requirement` example when you have one. Use `inconclusive` or `recollection_only` when appropriate. See the synthetic example for structure, not real findings.
4. Verify the manually selected client and reasoning-effort categories. Leave `unknown` when uncertain. Do not infer server-resolved model identity from the UI or token counters.
5. Only if you have reviewed public disclosure and hold the necessary rights/permissions, change both `consent` booleans to `true`. Real data must retain `synthetic: false`. The collector never supplies consent on your behalf.
6. Choose a new neutral filename such as `submissions/entry-0001.json`, without an employer, project, person, task ID or date that you do not intend to disclose. Fork/branch locally, then run:

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

Submit only the intended reviewed JSON or scoped code/docs changes. State whether data is synthetic, list the local checks you ran, and confirm you have the rights to release your contribution under MIT. Explain collection overlap or limitations using non-sensitive descriptions. Do not paste raw logs, original identifiers, prompts, credentials, private repository names or local paths into the PR, its title, commits or attachments. Git commit metadata and your GitHub account are public too. This is a de-identified data payload, not an anonymous submission. Do not name any repository in the payload, whether public or private; no naming exceptions apply.

By submitting, you agree to license your original contribution under the repository's MIT license. You must have the rights and permissions to share it publicly. Contributors retain their own copyright; downstream users must preserve applicable copyright and permission notices. Do not submit third-party material you cannot license. This project makes no legal guarantee about your particular data or situation.

Maintainers review the exact diff, schema, accounting, synthetic flag, consent and collection limitations before accepting a submission. A passed validator is not a finding that disclosure is safe or that a claimed observation is true. If anything sensitive appears, stop sharing it; removing a file later cannot guarantee removal from public copies.

## Questions and schema improvements

Use Discussions for public feedback, including experiences that contradict the hypotheses. A controlled vocabulary deliberately limits detail. Suggest additions with synthetic examples when it cannot capture your case safely. Schema changes need a version decision and local tests. Never upload session JSONL or SQLite to demonstrate a parser failure; construct a minimal synthetic fixture instead.

No GitHub Actions or connected CI may be added, triggered or required. Run all checks locally. Do not add production dependencies without approval.
