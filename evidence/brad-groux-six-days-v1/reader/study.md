> Editorial draft published for review. This is not a final article or a social post.

# When an established workflow meets GPT-6 Astra

## What I observed

The workflow I used with GPT-5.6 did not carry forward reliably to GPT-6. That is my experience from testing and day-to-day use. This study documents retained Astra activity and the steering recorded around it. It asks whether an established operating method remains dependable after a model upgrade.

Across six relative study days, the retained records contain 25,254 responses, 557 turns, and 3,420,584,663 total tokens. A separate contextual review identifies corrective steering in 147 of 538 substantive contributions. Those contributions form 78 correction episodes, 31 with repeated corrective contributions.

These observations support examining supervision and workflow continuity. They do not supply a matched GPT-5.6 baseline, a causal account of Astra's behavior, or a model failure rate. The large usage total does not resolve those limitations.

## The operating method predates this review

My documented method uses task scope, repository context, versioned SOPs, verification criteria, durable notes, and clear handoffs. Six articles describe its development:

| Published | Article | Relevant practice |
|---|---|---|
| June 13, 2026 | [Codex-maxxing: treating Codex like an operating loop](https://x.com/BradGroux/status/2065938280508432788) | Persistent workstreams, inspectable artifacts, verification before completion. |
| June 24, 2026 | [The Best Codex Upgrade I Made Was Treating Repeated Work Like a Product](https://x.com/BradGroux/status/2069785811017437672) | Prompt artifacts, preservation boundaries, retained decisions, stop conditions. |
| June 25, 2026 | [The Useful Part of Agentic Auto-Scheduling is the Feedback Loop](https://x.com/BradGroux/status/2070134268051763381) | External verification, result classification, bounded retries. |
| June 26, 2026 | [Stop Asking Codex to do Magic. Build the Harness.](https://x.com/BradGroux/status/2070510393126952992) | Task contracts, role boundaries, independent assignments and file ownership. |
| June 29, 2026 | [Using Codex or OpenClaw? Put Your SOPs Where the History Lives.](https://x.com/BradGroux/status/2071586981381832714) | Versioned standards, shared context, review and rollback; stale SOP risks. |
| July 1, 2026 | [Before Businesses Use Codex, Decide What It Can Access](https://x.com/BradGroux/status/2072313657883586873) | Access modes, task-specific privilege, configuration validation. |

Eric Provencher from OpenAI's Codex DX team describes substantially overlapping principles in [Practical multi-agent orchestration in Codex](https://x.com/pvncher/status/2080707291603407077), published July 24: distinct assignments, constraint preservation, delegation boundaries, and proportional reasoning effort for GPT-5.6.

This prior-generation guidance is central to the comparison. It establishes the kind of working method practitioners were encouraged to adopt. The articles do not prove identical configurations or that every later task loaded the correct instruction version. My firsthand account is that the method did not transfer reliably; a controlled comparative difference remains unmeasured.

## Three kinds of evidence

The study keeps measured activity, coded observations, and direct ratings separate.

**Measured activity** comes from retained native records and repository history. It describes recorded responses, tokens, turns and repository events. None of these measures directly evaluates correctness or satisfaction.

**Coded observations** come from contextual review of substantive contributions. Explicit dissatisfaction and corrective steering may overlap. Coding is interpretive and can be revised through adjudication.

**Direct ratings** would come from a participant explicitly reporting satisfaction or ease. No historical rating was inferred from these transcripts. There is no CSAT, ease score, or composite performance score in this study.

## Population and collection

This is one practitioner's observational case study using two retained local record stores. The frozen window covers six relative days, with the final day ending at a common cutoff. The calendar start was a requested study boundary, not independent proof of a global model release timestamp. Three measurement or coordination tasks were excluded.

Records were attributed to Astra using recorded turn context, not server-resolved model telemetry. An observer label identifies the store retaining a record; it does not establish where execution occurred. Records and identities were reconciled to avoid duplicate counting. This is not a comprehensive account billing export, and missing or unretained records may affect coverage.

Repository history covers the broader date window in 17 identifiable repositories associated with observed work. One of the 18 observed project identities remained unresolved. Context association does not prove that a repository was changed in that task. Repository events may come from any author, bots, references, and administrative activity.

Every project uses a stable generic label. The explorer contains no public joins back to named source projects. De-identification reduces disclosure but cannot guarantee anonymity: activity patterns can remain distinctive.

## Recorded usage

| Measure | Frozen-window value | Interpretation |
|---|---:|---|
| Responses | 25,254 | Native recorded responses; not an HTTP request count. |
| Turns | 557 | Includes 551 completed and 6 unfinished turns. |
| Native user-message items | 488 | Not guaranteed distinct human requests. |
| Task identities | 76 | Distinct retained identities after reconciliation. |
| Total tokens | 3,420,584,663 | Input plus output, with repeated context counted. |
| Input tokens | 3,409,595,316 | Includes cached input. |
| Cached input tokens | 3,348,480,640 | About 98.2% of input tokens. |
| Uncached input tokens | 61,114,676 | Input minus cached input. |
| Output tokens | 10,989,347 | Includes reasoning output. |
| Reasoning output tokens | 3,684,075 | A subset of output, not an additional total. |

The completed-turn durations sum to about 142.54 hours. Their interval union is about 83.11 hours after removing concurrency. Neither represents human hours saved. Unfinished turns are excluded from duration measures. Daily duration groups assign a completed turn's full duration to its start day; they are not calendar-day occupancy.

Unique task counts and interval unions cannot be summed across arbitrary groups. The explorer therefore uses additive response and token counters for filtered comparisons and leaves these non-additive whole-window measures in the study text.

## Repository activity

| Measure | Full-window value |
|---|---:|
| Active issues | 444 |
| Issues opened | 401 |
| Distinct issues with a close event | 385 |
| Distinct issues reopened | 3 |
| Active PRs | 452 |
| PRs opened | 435 |
| PRs merged during the window | 410 |
| First-parent commit objects | 396 |
| Repository-qualified paths changed in net boundary diffs | 3,753 |
| Text lines added in net boundary diffs | 311,765 |
| Text lines deleted in net boundary diffs | 18,415 |
| Net text-line change | +293,350 |

“Active” means created in the window or carrying at least one timestamped timeline event. A close event does not establish a verified fix and can be followed by reopening. At cutoff, the active PR population contained 411 merged PRs, 29 closed without merge, and 12 open. One of those 411 merged before the window, which explains the difference from 410 in-window merges.

The diffs compare immutable first-parent boundaries, using an empty-tree baseline where a repository was created in the window. They include documentation, tests, lockfiles, and other source or assets. Binary files do not contribute meaningful text-line counts. Net path changes are not cumulative touches. First-parent commit objects are not PR identities or necessarily branch landing events.

These figures are activity context, not verified Astra authorship or productivity. The repository dataset is available for the full window only; the explorer does not invent daily outcomes or allocate merges in proportion to token use.

## How the contextual review worked

Protocol 1.1 defines the unit as a substantive contribution after typed/voice reconciliation. A contribution can have multiple source components. The 538 units contain 396 typed contributions, 141 voice contributions, and one voice contribution with a typed reference. This differs deliberately from the native usage denominator.

The review distinguishes explicit dissatisfaction (D), corrective steering (C), routine contributions, and ambiguous material. D and C may coincide. A new request or preference is not automatically a correction. Profanity alone is insufficient to establish dissatisfaction with model work. Context was reviewed around disputed units, and both observers were reconciled against the same versioned rules.

The exclusive partition is 63 D-only, 56 C-only, 91 both, 310 routine, and 18 ambiguous: together, 538. Thus D is 154, C is 147, and the union is 210. That yields 28.62 D units, 27.32 C units, and 39.03 union units per 100 reviewed contributions. These describe the reviewed material, not independent trials or probabilities of model failure.

Correction episodes group related steering. Repetition means distinct corrective contributions in an episode. Episode counts are assigned to the day of the first corrective contribution; they do not count every day on which an episode continued. Process/SOP tags apply at episode level and can coexist with functional concerns.

The review found 78 correction episodes, including 31 repeated episodes. Forty episodes involved process or SOP concerns, linking 102 corrective contributions. Those 102 contributions are not individually demonstrated SOP violations.

## What was corrected and what was resolved

Selected retained examples involved repeated discussion of testing cadence, a request for a writing-guide location already supplied earlier, and a completion handoff that omitted requested work. One testing-related episode contained 17 corrective contributions and a later full-suite run. The record establishes intervention and the run; it does not establish that every rerun was unnecessary or calculate wasted tokens.

A deployment-direction dispute involved a stale runbook. This is a meaningful competing explanation: workflow documentation and model behavior both deserve scrutiny. Some other handoffs accurately disclosed remaining work; disclosed incompletion is not automatically false completion.

| Episode outcome under the review rubric | Episodes |
|---|---:|
| Confirmed resolved in the reviewed context | 14 |
| Accepted with residual issue or waiver | 3 |
| Fix reported, not independently verified | 15 |
| Claim withdrawn; artifact unverified | 1 |
| No closure established | 45 |

These outcomes sum to 78. “No closure established” is not proof that an issue remained unresolved forever. “Confirmed resolved” is bounded to the reviewed issue and available context, not independent certification of the entire deliverable. Acceptance of a prepared package does not establish every aspect of its quality.

## Related practitioner reports

Selected replies add context, without expanding the audit denominator:

- [Arbaz](https://x.com/arb5z/status/2096429348287029584) describes drift with a long design-system document and better results with fewer concrete references.
- [Billovskii](https://x.com/TheArcAge/status/2097291134976282752) describes behavior recurring after explicit prohibitions.
- [Christopher Comparán](https://x.com/ccomparanv/status/2097102158881493122) describes difficulty on projects with hard constraints.
- [John Collins](https://x.com/Yinielin/status/2097063165410369674) reports good instruction-following when steps are explained.
- [Nikhil Pareek](https://x.com/itsjustnikhil/status/2096419855004209603) describes a broader constrained-editing problem across models and proposes varying constraint counts.

These are illustrative, self-selected reports, not a representative survey. They do not establish identical configurations, matched comparisons, or the prevalence of the problem. The different experience and broader explanation remain part of the evidence.

## Two untested explanations

I suspect shortcuts toward completion can displace SOP or guideline adherence. I also suspect requirements can be lost during delegation, as described in [my handoff post](https://x.com/BradGroux/status/2097420111389098317). Both are entirely untested hypotheses based on roughly four or five days of personal experience. Efficiency is beneficial when it preserves the intended outcome and constraints.

Related safety research raises useful questions without establishing either explanation here. [OpenAI's incident report](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) concerns internal evaluations with reduced safeguards and an internal research model driving the principal compromise. It also describes excessive reasoning without score improvement, which does not support a simple token-minimization explanation. [Hugging Face's technical timeline](https://huggingface.co/blog/agent-intrusion-technical-timeline) reconstructs that particular intrusion. Neither documents a production Astra takeover.

A [DeepMind preprint](https://arxiv.org/html/2609.04170v1) describes a grading exploit spreading among agents through shared artifacts. Propagating a bad strategy differs from losing a requirement during delegation. Its evaluation does not establish either mechanism in Astra.

## Limits and robustness

The arithmetic, exclusive partitions, shared protocol, source reconciliation, and frozen inputs were checked. Those checks support internal consistency, not independent coding reliability. Contextual decisions were revised during reconciliation; the current result supersedes earlier observer-specific coding versions.

This study lacks randomized assignment, matched task difficulty, an independently coded comparison set, a controlled model baseline, comprehensive billing coverage, and a verified counterfactual. Contributions within a task are dependent, and high-intervention tasks can contribute many units. Small day or project groups are especially unstable and should not be ranked as model performance.

Instructions changed during the work. A later rule cannot be retroactively treated as an earlier requirement. Frontend voice-model identity is unknown; recorded Astra worker context does not identify the model responsible for every conversational mismatch. Outcome evidence is incomplete. These limits prevent a causal attribution or population estimate.

## What would make the next study stronger

A prospective comparison could use matched tasks and frozen instructions, record model and surface versions, define acceptance checks before execution, and counterbalance task order. It should record interventions and outcomes separately from response volume and cost.

A delegation test should trace each requirement through the actual assignment, accessible recipient context, resulting action, and correction. It should compare direct execution with bounded delegation while holding task scope constant and checking tool access and stale instructions.

An efficiency test needs an observable tradeoff and an independently defined acceptance bar. Finishing quickly while preserving all requirements is a success. Deviations should be judged against the original task contract, not inferred motives.

Independent coding and an adjudication log would help assess rubric reliability. Optional direct satisfaction and ease ratings should be collected prospectively, without manufacturing historical scores or combining them with token volume into a single index.

## Participate and inspect

The accompanying [local explorer](explorer.html) provides day and project comparisons while preserving the distinction between usage and coded observations. Repository comparisons remain explicitly full-window. Its source data is limited to reviewed, de-identified aggregates; raw records and alias mappings remain private.

The [MIT contribution kit](https://github.com/BradGroux/astra-field-study) contains synthetic examples, a bounded contribution format, and support for optional directly reported ratings. Its examples remain synthetic. Reviewed aggregates are published separately in the repository’s versioned evidence area; the contribution schema is narrower than this audit and cannot directly ingest the existing aggregate exports.

This is what I currently think, and I want to know more. Contrary experiences are especially useful. Use the kit's guidance or contact me through [Twitter](https://x.com/BradGroux). Publishing a real contribution should follow a deliberate review of its scope and privacy; the existence of a synthetic example does not establish anonymity.
