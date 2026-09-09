> Editorial draft published for review. This is not a final article or a social post.

# What broke when I carried my GPT-5.6 workflow into GPT-6

The workflow I used with GPT-5.6 did not carry forward reliably to GPT-6 Astra. That is my experience from testing and daily use.

I had already built the process around defined scope, repository context, versioned SOPs, meaningful verification, and a clear handoff. I wrote about the [operating loop](https://x.com/BradGroux/status/2065938280508432788), [task harness](https://x.com/BradGroux/status/2070510393126952992), and [SOPs](https://x.com/BradGroux/status/2071586981381832714) in June.

Eric Provencher from OpenAI's Codex DX team described closely aligned practices in [his July guidance for GPT-5.6](https://x.com/pvncher/status/2080707291603407077).

That is the point of the comparison. People built real working processes around the previous generation. We should evaluate whether those processes survive the upgrade.

## I checked the retained records

Across six study days and two local record stores, the audit identified:

- 25,254 responses across 557 turns.
- 3.42 billion recorded tokens, including 3.35 billion cached input tokens.
- 10.99 million output tokens, including reasoning output.

Cached input was about 98.2% of input. These are recorded counters, not unique text, billed spend, or useful work measured in tokens.

The observed repository population also had 410 PRs merged during the broader window across 17 identifiable repositories. That is repository activity, not proof that Astra authored all of it or that every change worked.

## What took steering

The separate contextual review contained 538 substantive contributions, reconciling typed and voice material.

147 contained corrective steering. 154 expressed explicit dissatisfaction. 91 contained both. The union was 210.

That is not a 27% failure rate. It is 147 corrective contributions under a stated rubric. It is not CSAT either: I did not supply historical satisfaction ratings, and none were inferred.

The corrections formed 78 episodes; 31 included repeated corrective contributions. Process or SOP concerns appeared in 40 episodes, linked to 102 corrective contributions. Those 102 are not individually proven guardrail violations.

The retained examples include reasserting testing cadence, pointing back to an already supplied writing guide, and challenging missing handoff work. A stale runbook also contributed to one dispute. The operating system around a model needs scrutiny too.

## The replies are useful context

[Arbaz described detailed design-system drift](https://x.com/arb5z/status/2096429348287029584). [Billovskii described repeated behavior after explicit prohibitions](https://x.com/TheArcAge/status/2097291134976282752). [Christopher Comparán described problems with hard constraints](https://x.com/ccomparanv/status/2097102158881493122).

[John Collins had better results when steps were explained](https://x.com/Yinielin/status/2097063165410369674). That belongs in the discussion too.

These are selected practitioner reports, not a survey or additional rows in my audit.

## What I suspect, and what I have not shown

I suspect shortcuts toward finishing can displace requirements. I also suspect requirements get lost during delegation, as I described in [my handoff post](https://x.com/BradGroux/status/2097420111389098317).

Both are entirely untested hypotheses from roughly four or five days of personal experience. Efficiency is useful when it preserves the outcome and constraints. The audit does not identify an optimization objective, locate a delegation failure, or measure a matched GPT-5.6/GPT-6 difference.

What I can say is that carrying my established method into Astra has taken repeated intervention. Businesses need to know what carries forward, what must change, and how to verify that the replacement process works.

I published a small MIT contribution kit with synthetic examples: [astra-field-study](https://github.com/BradGroux/astra-field-study). Its examples remain synthetic; reviewed aggregates are available separately in the repository’s versioned evidence area. Optional ratings are kept separate from measured activity and coded observations.

This is what I currently think. I want more evidence, especially experiences that contradict mine. If your established workflow transferred cleanly, help make that comparison concrete.
