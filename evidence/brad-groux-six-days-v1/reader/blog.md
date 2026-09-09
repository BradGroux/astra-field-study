> Editorial draft published for review. This is not a final article or a social post.

# My GPT-5.6 workflow did not carry forward reliably to GPT-6

I expected a model upgrade. I did not expect to spend so much time reasserting the way I work.

The workflow I used with GPT-5.6 did not carry forward reliably to GPT-6 Astra. That is what I have seen in my own testing and day-to-day use. The recurring problem has been keeping the work inside the agreed process: use the supplied context, follow the SOP, verify what matters, and finish the requested handoff.

That process was already documented. In June, I wrote about [treating Codex as an operating loop](https://x.com/BradGroux/status/2065938280508432788), [building a harness around the work](https://x.com/BradGroux/status/2070510393126952992), and [keeping SOPs in versioned files](https://x.com/BradGroux/status/2071586981381832714). I was trying to make repeated work dependable enough to use in a business.

Eric Provencher from OpenAI's Codex DX team later described closely aligned practices in his [July 24 article on GPT-5.6 orchestration](https://x.com/pvncher/status/2080707291603407077): distinct assignments, preserved constraints, bounded delegation, and reasoning effort appropriate to the task.

The generation matters. That guidance gives us a reference for the operating methods people were encouraged to build around GPT-5.6. My question is what happens to those investments when the next model arrives.

## I wanted records behind the complaint

I reviewed retained Astra records from two local stores across six study days, ending at a fixed cutoff. After reconciliation and exclusions, they contained 25,254 responses across 557 turns.

The recorded total was 3,420,584,663 tokens. That sounds enormous, but the composition matters: 3,348,480,640 were cached input tokens. Cached input accounted for about 98.2% of input tokens. Output was 10,989,347 tokens, including reasoning output.

Those are native recorded counters. They are not unique words, an account billing export, or a measure of useful work. Repeated context is counted repeatedly. I cannot turn that token total into money spent or human hours saved.

I also reviewed repository activity across the observed project population. Seventeen identifiable repositories had 410 PRs merged during the broader window. Their complete net boundary diffs contained 3,753 repository-qualified changed paths, with 311,765 added and 18,415 deleted text lines.

That establishes activity around this work. It does not establish that Astra authored every change, that every closed issue was fixed, or that more lines meant better software. All source projects use generic labels in the accompanying explorer.

## The steering is the part I wanted to understand

A separate contextual review coded 538 substantive contributions. This denominator differs from the 488 native user-message items in the usage record because the review reconciles typed and voice material, excludes non-substantive material, and joins components belonging to the same contribution.

Of those 538 contributions:

- 147 contained corrective steering.
- 154 expressed explicit dissatisfaction.
- 91 contained both, so 210 contained either or both.

The categories overlap. Adding 147 and 154 would count 91 contributions twice.

These are observations under a coding rubric, not a model failure rate or a satisfaction survey. A correction can follow an actual deviation, a misunderstanding, conflicting instructions, or a change in what the user wants. The review used context to distinguish a new request from a correction, but judgment remains part of the process.

The corrections formed 78 episodes. Thirty-one contained repeated corrective contributions. Of the 147 corrective contributions, 102 linked to 40 episodes involving process or SOP concerns. That does not mean 102 individually proven SOP violations: an episode can contain several kinds of problem.

In the retained examples, I had to reassert testing cadence, point back to a writing guide supplied earlier, and challenge a handoff that omitted requested work. One testing-related episode contained 17 corrective contributions. Some reruns may have been necessary; this audit does not calculate wasted tests or wasted tokens.

There was also a dispute involving stale deployment instructions. That belongs in the account because the surrounding system can contribute to the problem. An operating method depends on its documentation being current.

## Other people described related friction

The replies to my posts are not a survey, but some are specific enough to be useful context.

[Arbaz described drift under a detailed design-system document](https://x.com/arb5z/status/2096429348287029584). [Billovskii described behavior recurring after explicit prohibitions](https://x.com/TheArcAge/status/2097291134976282752). [Christopher Comparán described difficulty with hard constraints](https://x.com/ccomparanv/status/2097102158881493122).

There were different experiences too. [John Collins reported good instruction-following when steps were explained](https://x.com/Yinielin/status/2097063165410369674). [Nikhil Pareek framed constrained editing as a broader problem across models and proposed varying the number of constraints](https://x.com/itsjustnikhil/status/2096419855004209603).

These accounts help identify questions worth testing. They do not establish how common the problem is, and I have not verified that these practitioners used my configuration.

## Two explanations I want to test

My first suspicion is that shortcuts toward completion can displace requirements. Efficiency is useful when the intended outcome and constraints survive. Efficiency itself is not cheating. I have not established Astra's optimization objective or shown that it explains these observations.

My second suspicion is that requirements get lost during delegation. I described that experience in [this post about agent handoffs](https://x.com/BradGroux/status/2097420111389098317). To test it, I would need to trace a requirement through the actual assignment, the receiving agent's accessible context, its action, and the correction, while checking for stale instructions and tool limits.

Both explanations are entirely untested hypotheses based on roughly four or five days of personal experience. A large token count does not make them more certain.

## What I want from a model upgrade

My firsthand conclusion is that this established workflow has required more intervention than I expected with Astra. I have not measured a matched GPT-5.6-versus-GPT-6 difference. Those are separate statements, and both matter.

For business use, I want to know whether a model can preserve an operating method through the whole task: after the first correction, after a handoff, and at delivery. If the recommended method needs to change, we need a clear migration path and evidence that it restores reliability.

I have put a [small MIT contribution kit on GitHub](https://github.com/BradGroux/astra-field-study). It contains synthetic examples and a way to prepare bounded contributions, including optional directly reported ratings. Its examples remain synthetic. The reviewed aggregates are now available separately in the repository’s versioned evidence area; the contribution schema does not accept the audit exports directly.

This is what I currently think. I want to know more. If your experience contradicts mine, especially under comparable constraints, that is useful evidence. Start with the kit or contact me through [Twitter](https://x.com/BradGroux).
