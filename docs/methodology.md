# Methodology and metric definitions

This kit supports the native Codex JSONL record shape observed in retained September 2026 histories: `session_meta`, `turn_context`, `token_usage_record`, and `event_msg` containing completed `UserMessage` items. This is an observed client format, not a stable vendor API contract. No server-resolved model telemetry or billing data is available here. Format changes may require a reviewed adapter and new synthetic tests.

## What the collector does

It freezes file byte lengths before reading local `sessions/**/*.jsonl` and `archived_sessions/**/*.jsonl`. It does not follow explicitly symlinked input files or source roots. It is not an atomic cross-file snapshot. Model attribution requires the explicit response turn ID to have one unambiguous recorded model context. Current session defaults and the UI model selector are not attribution evidence.

Responses deduplicate by native response ID across files in memory; conflicting ownership or token values reject the export. The earliest retained replay timestamp determines the date. Session IDs are not response IDs: child-agent responses can reference a parent session and remain distinct responses. UserMessage items deduplicate by native item ID. Other record types and cumulative token snapshots are never added as model responses. No fallback differences of cumulative counters are used.

Only per-response records for the selected model in the inclusive UTC date window enter response totals. Message counts include only native UserMessage items in that window associated with turns that have included responses. A message for a turn with no included response is outside this metric. Unknown model context, incomplete JSON, partial trailing lines, unsupported token fields and conflicting identities stop collection with a generic error. This deliberately favors a missing submission over invented accounting.

## Fields

| Field | Meaning and limits |
|---|---|
| `schema_version` | Public contract version, `1.0` for activity/observations; `1.1` optionally adds direct ratings. Both are supported. Unexpected fields or versions are rejected. |
| `synthetic` | Whether this is invented demonstration data. The initial example is synthetic; the collector sets false. |
| `consent` | Two explicit contributor acknowledgments for reviewed public release and rights/MIT licensing; default false. |
| `setup.model` | Model attributed from matching turn context, not confirmed by server response or billing. |
| `setup.client`, `reasoning_effort` | Contributor-supplied categories; unknown by default. They are not inferred from raw text. |
| `setup.observer_scope` | One local retained store. Not proof of execution host, one person, or complete account activity. |
| `window.requested_days` | Length of the requested UTC-date window. Actual dates stay local. May include partial days or gaps; not uninterrupted coverage. |
| `responses` | Distinct included native response IDs. Not all network requests, retries, human prompts or tasks completed. |
| `turns_with_responses` | Distinct turn IDs with included response records. May include continuations and subagents. |
| `tasks_with_responses` | Distinct native thread IDs with included response records. Not necessarily independent user assignments. |
| `native_user_message_items` | Distinct completed native UserMessage items on included turns; not verified human-authored requests. |
| `repository_contexts_with_responses` | Distinct exact recorded Git URL strings, falling back to CWD strings; missing values excluded. No names exported. Different URL spellings or paths may describe the same repo; a context is not proof the repo was changed. |
| `input_tokens` | All recorded input tokens, including cached input. Repeated context is counted repeatedly. |
| `cached_input_tokens` | Subset of input served from cache; never add again to input. |
| `cache_write_input_tokens` | Native cache-write counter reported separately; not added to total or treated as billed cost. |
| `output_tokens` | All output, including reasoning. |
| `reasoning_output_tokens` | Subset of output; never add again. |
| `total_tokens` | Input plus output. Not unique words, source-code volume, subscription allowance or spending. |
| `daily` | Events grouped by UTC event date internally, exported as `day_index` starting at 1 for the requested start date; actual dates stay local. Response/message/token totals add; distinct turn/task/context counts can overlap across days. Only relative days with included responses or messages are emitted. |
| `duplicate_response_records` | Replayed selected-model response records encountered in the requested window and removed; diagnostic only. |
| `ignored_counter_snapshots` | All token_count snapshots encountered in the window, across models; ignored for accounting. |
| `observations` | Optional controlled-category practitioner labels, never inferred from counts. Not a representative failure-rate denominator. |

No runtime, issues closed, merged PRs, line changes, productivity or monetary metrics are inferred. Those need separate outcome evidence and a defined scope. Raw identifiers stay local, so aggregate submissions cannot be deduplicated against each other: do not simply sum overlapping windows, shared stores or exports from multiple machines.

## Adherence observations and hypotheses

Select a requirement category and record behavior separately from its outcome. `instruction_access` distinguishes confirmed recipient context from available-but-unconfirmed material or an absent handoff. `delegation` distinguishes actual use from uncertainty. `evidence_basis` distinguishes a local action/outcome review from recollection. `alternatives_considered` must include at least one category; `unknown` honestly represents unresolved alternatives.

A report labeled `lost_requirement_after_handoff` is the contributor's observation classification, not a demonstrated causal effect of delegation. Missing context, ambiguous instructions, client behavior, tool limitations and task difficulty can explain apparent failures. Include successful adherence. The two initial explanations remain entirely untested hypotheses based on a short personal observation window. Repeated reports may motivate a controlled study; they cannot establish internal motives or causal productivity effects on their own.


## Three separate evidence layers

Measured activity is distinct from contextual observation coding and optional direct participant ratings. Observations remain judgments with their own sampling and evidence limits; they do not establish CSAT. No complaint or correction does not mean satisfaction. Do not subtract corrective requests from 100 and call the remainder satisfied, infer ratings from text, or combine these dimensions into a weighted quality index.

Schema `1.1` adds optional `self_reports` while preserving existing `1.0` submissions and collector output. See the [rating protocol, denominators and migration instructions](self-reported-ratings.md). The preview keeps actual satisfaction/ease distributions and timing cohorts separate, reports missingness and response coverage, and calculates conventional CSAT only from valid satisfaction answers. Repeated attempts within one person are clustered observations. Self-selection, recall and missing responses limit interpretation; aggregate payloads cannot establish unique participant identity across contributions. Do not treat task ratings as independent people or infer causal/general-population results.
