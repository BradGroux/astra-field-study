# Reviewed aggregate submissions

There are no participant submissions here yet. The examples in `examples/` are synthetic. The separately reviewed real case in [evidence/](../evidence/study-0001-v1/README.md) uses a different versioned format and does not alter the submission contract.

Follow [the contribution guide](../CONTRIBUTING.md). Use neutral filenames and submit only allowlisted JSON that passes `tools/validate.py --ready` after full manual review and consent. Do not include a private alias map or raw evidence. Avoid duplicate or overlapping windows; cross-submission identity deduplication is intentionally unavailable.

## Submission checklist

1. Follow [Prepare locally](../CONTRIBUTING.md#prepare-locally), including full-file review and both consent fields.
2. Validate and canonicalize one aggregate to a new neutral JSON filename in this directory. Use schema 1.0, or 1.1 for actual optional participant ratings.
3. Follow [Open a pull request](../CONTRIBUTING.md#open-a-pull-request) to submit from your fork to `BradGroux/astra-field-study:main`. Include local verification and non-sensitive coverage/overlap limitations.
4. Wait for maintainer review. Validator success alone does not establish safe disclosure or a true finding.

For experiences that cannot fit the schema, start a [Discussion](https://github.com/BradGroux/astra-field-study/discussions) without uploading private evidence. Use synthetic examples when proposing new fields.
