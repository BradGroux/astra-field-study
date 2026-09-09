# Optional task satisfaction and ease ratings

Keep three evidence layers separate: **measured activity**, **coded observations**, and **direct participant ratings**. A token count is activity, a judged instruction deviation is an observation, and a satisfaction answer is a self-report. None substitutes for another. Do not calculate a blended or weighted quality index, infer historical ratings from transcripts, or treat silence as satisfaction.

Ratings are optional. Include ordinary work, successful adherence and counterexamples as well as difficult experiences. Decide which task attempts are eligible before seeing their results when possible. Ask after an attempt ends, including an unsuccessful attempt. The unit is a human task attempt, not a native response, turn, issue, test or completed-task claim.

## Ask both questions

Use the same wording and anchors for every included attempt:

| Dimension | Question | Responses |
|---|---|---|
| Satisfaction | How satisfied were you with the help you received on this task? | 1 Very unsatisfied; 2 Unsatisfied; 3 Neutral; 4 Satisfied; 5 Very satisfied |
| Task ease (SEQ) | How easy or difficult was it to complete this task? | 1 Very Difficult through 7 Very Easy; label the endpoints |

Let the participant skip either question. Record a skipped or unavailable answer as `null`, never zero, a midpoint or an inferred value. Do not let an assistant answer on the participant's behalf. Satisfaction concerns the help received; ease concerns the task experience and can reflect tool problems, task difficulty and other factors beyond the model.

The satisfaction item adapts conventional five-point CSAT to this context; it is not a newly validated agent-quality instrument. Conventional CSAT counts ratings 4 and 5 among valid answers. [Qualtrics CSAT guidance](https://www.qualtrics.com/articles/customer-experience/what-is-csat/).

The ease item uses the current SEQ wording and seven-point endpoint anchors described by its researchers. SEQ is normally administered immediately after a task attempt. [MeasuringU on question wording](https://measuringu.com/is-it-ok-to-edit-the-wording-of-standardized-ux-questions/), [SEQ administration](https://measuringu.com/seq10/). The linked publisher search extracts supplied the SEQ wording and administration guidance during this update; direct page retrieval was unavailable. Linked sources retain their own terms.

## Separate timing and preserve denominators

Schema `1.1` adds an optional `self_reports` object. The usage collector continues to emit `1.0` with no ratings. A participant may manually upgrade a local draft to `1.1` and supply actual ratings using the [synthetic example](../examples/synthetic-ratings-submission.json). The validator accepts both versions; existing `1.0` files do not need migration. A `1.1` file without `self_reports` is also valid. Older `1.0`-only tools will reject `1.1`; use the updated validator. Never add the new field to a file still labeled `1.0`.

`protocol` is `post_task_v1`. `participant_scope` is `one_self_reporting_participant`: all ratings in one contribution come from one person about their own attempts with the setup being reported. Do not pool different people into that object. The payload has no participant, machine or original task identifier.

Each `groups` entry has one unique timing category:

- `immediately_after_task`: asked and answered directly after the attempt, while the experience is fresh.
- `retrospective_recollection`: a later rating supplied from memory. It must be a real answer; a historical chat label is not a rating.
- `unknown`: timing cannot be established. Keep it separate rather than guessing.

An attempt appears in only one group and once in `ratings`; if it was already rated immediately, do not add its later recollection as another observation. Group rows are separate cohorts, not repeated ratings of the same attempt. Keep any deduplication notes local and outside the submission. The validator cannot verify this provenance without private identifiers.

For each group:

| Field | Meaning |
|---|---|
| `eligible_task_attempts` | Count of attempts in the chosen study window eligible for this timing cohort; `null` if unknown. Do not invent it from native task or turn counts. |
| `invited_task_attempts` | Count of distinct eligible attempts for which the participant was invited to answer **both** questions under this protocol; `null` if invitations were not tracked. A self-administered prompt counts as an invitation. |
| `ratings` | One object per recorded attempt, containing `satisfaction` (integer 1–5 or `null`) and `task_ease` (integer 1–7 or `null`). No IDs, dates, project labels or free text. An object with both values `null` records an unanswered invitation. |

The protocol offers both questions together. A collection that invited different questions to different sets of attempts cannot use one shared invitation count; leave that count unknown or propose a synthetic schema extension. Do not backfill untracked invitations merely because an answer exists. A known invitation count may exceed the number of recorded rows when some unanswered invitations were not individually recorded. It may never be smaller. Known eligibility must be at least the known invitations and recorded rows. Zero is a known zero; `null` is unknown.

A task attempt is not necessarily a native task ID, and retained activity may be incomplete. Rating counts are therefore not validated against `tasks_with_responses`. Keep the rating scope within the stated study window and setup, and explain scope limits without private detail. If no ratings were collected, omit `self_reports`; if invitations were tracked but unanswered, retain known counts and null answers or an empty array. The collector does not create either case automatically.

## Read the results

Run the usual local validator with `--preview`. The preview reports each timing group separately, with:

- Counts for all five satisfaction responses and all seven ease responses, ordered low to high.
- Valid answers, recorded unanswered rows, and invitations without an answer when invitation counts are known.
- Response coverage = valid answers / invited attempts × 100 for each dimension. Unknown or zero invitations produce `null` coverage.
- Eligible coverage = valid answers / eligible attempts × 100 when eligibility is known and nonzero.
- CSAT = satisfaction ratings 4 or 5 / valid satisfaction answers × 100. No valid answers produce `null`, not zero satisfaction.

For example, three satisfaction answers of 4, 5 and 2 produce CSAT 66.67%. With five invitations, response coverage is 60%. Those two percentages have different denominators. Ease stays a separate distribution, with no synthetic satisfaction conversion. The preview is a summary; review the entire JSON before consent or publication.

## Interpretation and contribution limits

Many ratings from one person are repeated measures, not many independent participants. Analyze distributions per contribution and timing cohort first. Cross-contribution participant identity and overlap are not recoverable from these payloads; do not assume one contribution equals one distinct person or pool rows as independent people. State participant counts and coverage only when they are actually known from an appropriately consented study design. Privacy-preserving contributions do not establish population representativeness.

Voluntary, self-selected contributions can overrepresent unusually good or bad experiences. Retrospective recall, unanswered invitations, untracked eligibility, task mix and incomplete local retention limit comparisons. Higher satisfaction can coexist with substantial corrective effort. A rating cannot establish that instructions were followed or the work succeeded; keep outcome evidence and coded observations separate. These records support descriptive exploration, not causal effects, general-population claims or normative agent rankings.

No ratings are inferred by the collector, and no tool uploads data. Public-release review and MIT-rights consent remain explicit. Never add raw histories, source IDs or hashes, exact dates/timestamps, repository or machine names, private paths, or freeform descriptions to a rating. See [privacy](privacy.md) and [contribution instructions](../CONTRIBUTING.md).
