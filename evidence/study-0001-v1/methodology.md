# Methods and interpretation

## Study question and scope

Brad reports that the operating method he used with GPT-5.6 did not carry forward reliably to GPT-6 Astra. His earlier public methods and Eric Provencher's GPT-5.6 guidance describe overlapping practices: scoped assignments, preserved constraints, bounded delegation, durable context, and appropriate verification. The difference in model generation is central to the continuity question, not a reason to dismiss it. The [source references](sources.md) document that context.

This is one practitioner's retained-record observational case study. It covers six relative study days across two record stores, ending at a frozen common cutoff. The final day is partial. The calendar start was a requested study boundary, not independent proof of a global release timestamp. Three measurement or coordination tasks were excluded. No new experiment or matched model comparison was performed for this evidence release.

The data separates measured activity, coded observations, and optional direct ratings. Repository events are measured activity with a different population and attribution limit. Direct ratings were not collected for this case, and none were reconstructed. There is no composite quality index.

## Recorded usage

Model attribution comes from recorded turn context, not server-resolved telemetry. An Observer label identifies the store retaining the records; it does not prove where execution occurred. Reconciliation removed duplicate response and native identities within the reviewed population. This is not an account-wide billing export, and unretained records may be absent.

- `responses`: native recorded responses, not HTTP calls.
- `turns`: completed and incomplete native turns. The total is 557 = 551 completed + 6 incomplete.
- `native_user_messages`: 488 native items, not guaranteed distinct human requests.
- `tasks`: 76 distinct retained task identities, exported only as counts.
- `tokens`: per-response counters. Input includes cached input; output includes reasoning output. Total = input + output. Uncached input = input − cached input. Repeated context is counted repeatedly.
- `sum_completed_turn_ms`: completed durations summed without removing concurrency, approximately 142.54 hours overall.
- `completed_interval_union_ms`: union of completed intervals, approximately 83.11 hours overall. This removes concurrency within its group. Neither duration measure represents human hours saved.

The public version represents interval union in integer milliseconds, an exact conversion from the source aggregates' millisecond precision. Incomplete turns are excluded from both duration measures. Daily grouping assigns the full completed duration to the turn's start day, not to the calendar time occupied within that day.

Task counts and interval unions are non-additive across arbitrary groups. The validator checks bounds instead of summing them as if they were additive. The reader therefore filters only additive response/token counters and coded contribution counts. It does not reconstruct union runtime from anonymous cells.

All 3,420,584,663 recorded tokens include 3,348,480,640 cached input tokens. Cached input is about 98.21% of input tokens, not of output. Output is 10,989,347 tokens, including 3,684,075 reasoning output tokens. These counters do not establish cost, unique text, useful work, or either causal hypothesis.

## Contextual coding, protocol 1.1

The unit is a substantive contribution after typed/voice reconciliation. One contribution can have multiple source components. There are 396 typed contributions, 141 voice contributions, and one voice contribution with a typed reference. Source components and their identities are not public.

Explicit dissatisfaction (D) and corrective steering (C) can overlap. A new request or first preference is not automatically a correction. Profanity alone does not establish dissatisfaction with the model's work. Context was reviewed around disputed contributions, and both record stores were reconciled against the same versioned rules. This is contextual judgment, not independently established coding reliability.

| Exclusive category | Units |
|---|---:|
| D only | 63 |
| C only | 56 |
| Both D and C | 91 |
| Routine | 310 |
| Ambiguous | 18 |
| Total | 538 |

D = 154, C = 147, and the union = 210. The corresponding per-100 counts are 28.62, 27.32, and 39.03. These describe the reviewed contributions, not independent attempts or probabilities of model failure. The public JSON stores counts rather than redundant rounded rates; the reader calculates rates using the selected contribution denominator. A zero denominator produces an unavailable rate, not zero satisfaction.

Correction episodes group related steering. There are 78 episodes, with 31 containing repeated corrective contributions. Episode counts, repetition flags, process flags, and outcomes are assigned to the first corrective contribution's day and project; an episode can continue beyond that group. Per-day episode counts are therefore onset counts, not counts of every episode active on the day.

Forty episodes involve process or SOP concerns and link to 102 corrective contributions. An episode can mix process and functional issues. Those 102 contributions are **not** individually demonstrated SOP violations.

| Bounded episode outcome | Count |
|---|---:|
| Confirmed resolved in the reviewed context | 14 |
| Accepted with residual issue or waiver | 3 |
| Fix reported, not independently verified | 15 |
| Claim withdrawn; artifact unverified | 1 |
| No closure established | 45 |

The outcomes sum to 78. No closure established does not mean an issue remained unresolved forever. Confirmed resolution is bounded to the reviewed concern and context, not independent certification of the entire product. Package acceptance does not establish all aspects of artifact quality.

Selected existing examples include reasserting testing cadence, pointing back to an already supplied writing guide, and challenging missing handoff work. One testing-related episode contains 17 corrective contributions and a later full-suite run. The audit does not establish that every rerun was unnecessary or calculate wasted tokens. A stale runbook also contributed to a deployment-direction dispute. Some other handoffs accurately disclosed remaining work. These alternatives prevent treating every intervention as model misconduct or false completion.

## Repository activity

There are 18 generic project labels in recorded usage. Seventeen repository identities were resolved and queried; one remains unresolved. All queries cover the full broader date window and include all authors. A repository associated with task context is not proof that a specific task changed it.

“Active” means created in the window or carrying a timestamped timeline event in it. Events can include references, bots and administrative actions. Opened records use creation timestamps. Close-event counts identify distinct records with a close event; they can reopen later. An issue close is not a verified fix. Candidate records reflect the selected active population in this snapshot.

There were 444 active issues, 401 opened, 385 with a close event, and 3 reopened. There were 452 active PRs, 435 opened, and 410 merged within the window. At cutoff the active PR population contained 411 merged, 29 closed without merge, and 12 open. One of the 411 merged before the window. The 410 in-window merges and 411 cutoff merged state are intentionally different.

Net diffs compare immutable first-parent boundaries, with an empty-tree baseline for repositories created in the window. They contain 3,753 repository-qualified changed paths, +311,765 and −18,415 text lines, net +293,350. This includes documentation, tests, dependency locks, and other source or assets, including generated/vendor paths where present. Classification is path-based; `other_source_or_asset` is not synonymous with application code. Binary files lack meaningful text-line counts. Missing event rows are normalized to zero only for identified repositories whose queried population has no issue/PR events; an unresolved repository is kept absent, not represented as zero activity.

The 396 first-parent commit objects use committer time. They are not PR identities or necessarily the time a branch acquired each object. Net changed paths are not cumulative touches. Repository totals do not establish Astra authorship or productivity, and no daily outcome cube is available. The explorer's day filter deliberately does not affect repository outcomes; its project filter does.

## Explanations remain untested

The observer suspects that shortcuts toward finishing may displace constraints and that delegation may lose requirements. Both are entirely untested hypotheses from roughly four or five days of personal experience. Efficiency is beneficial when it preserves the intended outcome and constraints. Large token or repository totals do not validate a mechanism.

External incident reports and multi-agent evaluation research provide context, not causal evidence for this case. Propagating a bad strategy differs from losing a requirement. The [source notes](sources.md) distinguish these claims and include contrary practitioner experiences.

## Limits and future comparison

The arithmetic, exclusive partitions, common coding protocol, deduplication and frozen inputs were checked. Those checks do not establish independent coding reliability, complete account coverage, or causal attribution. Contributions within a task are dependent, and high-intervention tasks can contribute many units. Small day/project groups should not be ranked as model performance.

There is no randomized assignment, matched task difficulty, controlled GPT-5.6 baseline, independently coded comparison set, or verified counterfactual. Instructions changed during the work; a later policy cannot be treated as an earlier requirement. Frontend voice-model identity remains unknown, so recorded Astra worker context does not identify the model responsible for every conversational mismatch. Outcome evidence is incomplete.

A prospective study should freeze instructions and acceptance checks, record model/surface versions, counterbalance matched tasks, trace actual delegation context, examine competing explanations, and collect optional direct ratings prospectively. Independent coding and aggregate-level adjudication notes would strengthen reliability. Contrary experiences and successful adherence should be invited equally.

## Disclosure boundary

The public data consists of controlled categories and aggregate counts with relative days and stable generic project/observer labels. No raw source text, private titles/URLs, task or session IDs, source-identity hashes, exact execution timestamps, machine paths, mappings, or joins to named projects are provided. Public methods/reply URLs identify their public authors, not anonymous project rows. De-identification is not a guarantee of anonymity; the author is intentionally named, and activity patterns can be distinctive.
