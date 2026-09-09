> Editorial draft for review.

# My GPT-5.6 workflow hasn't carried over reliably to Astra

In my testing with GPT-6 Astra, I've had to keep correcting work that was already covered by my instructions. That has included pointing back to a writing guide supplied earlier, reasserting when tests should run, and asking for requested work missing from a completion handoff.

I use Codex for ongoing work with documented scope, repository context, standard operating procedures, and verification before delivery. When I have to repeat those instructions during a task, that adds supervision. I wanted to understand how often that was happening in my own records, so I reviewed six days of Astra activity and the conversations around it.

## The process was already documented

In June, I wrote about [using Codex for ongoing work](https://x.com/BradGroux/status/2065938280508432788), [setting up the task and its constraints](https://x.com/BradGroux/status/2070510393126952992), and [keeping SOPs in versioned files](https://x.com/BradGroux/status/2071586981381832714).

Eric Provencher from OpenAI's Codex DX team described closely aligned practices in his [July article on GPT-5.6 orchestration](https://x.com/pvncher/status/2080707291603407077). His guidance covers distinct assignments, preserving constraints when delegating, and choosing reasoning effort to fit the work.

## What needed correction?

The review identified 147 corrective contributions among 538 substantive contributions from me. A contribution is a message or a reconciled piece of voice input, so several can belong to the same problem. The corrections grouped into 78 episodes, and 31 of those needed repeated corrective contributions.

Forty episodes involved process or SOP concerns. One testing-related episode alone contained 17 corrective contributions. The retained record shows the repeated intervention, although it doesn't establish that every test rerun was unnecessary.

The review also identified 154 contributions expressing dissatisfaction. Ninety-one of those included corrective steering.

<!-- figure: steering-partition -->

The review applied [a coding rubric](study.html#how-the-contextual-review-worked) to the conversations. Several corrections can address one problem, so these counts don't measure a model failure rate.

## How much work was in the records?

The retained records contained 25,254 responses across 557 turns. Recorded tokens totaled 3.42 billion, including 3.35 billion cached input tokens. Cached input accounted for 98.2% of input tokens; output totaled 10.99 million tokens, including reasoning. The large total includes repeated context, so it can't tell us how much useful work was completed or what it cost.

<!-- figure: responses-by-day -->

Across 17 identifiable repositories associated with the work, 410 PRs merged during the broader window. That count includes all authors. The [explorer](explorer.html) lets you inspect the activity and corrections by relative day and generic project label, with repository activity shown separately for the full window.

## What might explain it?

I have two hypotheses from roughly four or five days of personal experience: shortcuts toward finishing may displace requirements, and requirements may get lost when work is delegated. Both are entirely untested. The audit records the intervention; it doesn't establish either cause or a matched difference between GPT-5.6 and GPT-6. A deployment runbook contained outdated instructions.

Other practitioners described related problems in replies to my posts. [Arbaz reported drift with detailed design instructions](https://x.com/arb5z/status/2096429348287029584), and [Billovskii described behavior recurring after explicit prohibitions](https://x.com/TheArcAge/status/2097291134976282752). [John Collins reported good instruction-following when the steps were explained](https://x.com/Yinielin/status/2097063165410369674).

## Help make the comparison useful

I've published the reviewed aggregates, methods, figures, and a contribution kit in [Astra Field Study](https://github.com/BradGroux/astra-field-study) under MIT. The kit produces a local aggregate for review before submission. Project labels and days are generic, and raw conversations stay private. GitHub contributions still identify the contributor's account.

This is what I currently think, and I want to know more. If your established workflow transferred cleanly to Astra, I'd like to understand the instructions, task boundaries, and checks that made it work. You can contribute through the repo or [reach me on Twitter](https://x.com/BradGroux). Successful examples and experiences that contradict mine are welcome.
