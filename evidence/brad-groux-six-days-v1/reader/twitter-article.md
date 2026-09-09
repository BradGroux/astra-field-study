> Editorial draft for review.

# What I'm seeing with GPT-6 Astra and my existing workflow

I've been using GPT-6 Astra with the workflow I developed around GPT-5.6: documented task scope, repository context, standard operating procedures, and verification before delivery. In my testing, I've had to keep correcting work those instructions already covered. Examples included pointing back to a supplied writing guide, reasserting testing cadence, and asking for requested work missing from a completion handoff.

I reviewed six days of retained Astra records to understand the activity and the steering around it. The records contained 25,254 responses across 557 turns. A separate review of my typed and voice contributions identified 147 corrective contributions among 538 substantive contributions, grouped into 78 episodes. Thirty-one episodes contained repeated corrections.

## The process predates Astra

I wrote about [ongoing Codex work](https://x.com/BradGroux/status/2065938280508432788), [task scope and constraints](https://x.com/BradGroux/status/2070510393126952992), and [versioned SOPs](https://x.com/BradGroux/status/2071586981381832714) in June. Eric Provencher from OpenAI's Codex DX team described closely aligned practices in his [July guidance for GPT-5.6](https://x.com/pvncher/status/2080707291603407077), including distinct assignments and preserving requirements when delegating.

My established method hasn't carried over reliably in my Astra testing. The instructions cover access, testing, and delivery requirements for the work.

## What the review shows

Forty correction episodes involved process or SOP concerns. One testing-related episode contained 17 corrective contributions. The review also recorded 154 contributions expressing dissatisfaction, with 91 overlapping the corrective category. The same problem sometimes generated several corrections, so this count doesn't measure a model failure rate.

The usage total was 3.42 billion recorded tokens, including 3.35 billion cached input tokens. About 98.2% of input came from cache. Repeated context contributes to those counters, so the total doesn't tell us how much useful work was completed or what it cost. The study includes the full breakdown and keeps repository activity separate.

## Two hypotheses to test

I suspect shortcuts toward finishing can displace requirements, and requirements can get lost during delegation. Both are entirely untested hypotheses based on roughly four or five days of personal experience. I haven't run a matched GPT-5.6/GPT-6 comparison or traced a causal delegation failure. A deployment runbook contained outdated instructions.

The replies have included different experiences. [Arbaz reported drift under detailed design instructions](https://x.com/arb5z/status/2096429348287029584), while [John Collins reported good instruction-following when steps were explained](https://x.com/Yinielin/status/2097063165410369674).

I've published [Astra Field Study](https://github.com/BradGroux/astra-field-study) with reviewed aggregates, methods, figures, an explorer, and an MIT contribution kit. The kit keeps raw conversations private and lets contributors review their aggregate before submitting it. Optional satisfaction and ease ratings are collected directly and kept separate from usage.

This is what I currently think, and I want to know more. If your existing workflow transferred cleanly, share what you used and how you verified the result. Contribute through the repo or reach out here, especially if your experience contradicts mine.
