# Brad Groux's six-day Astra case study — evidence version 1

**The reported finding is a loss of workflow reliability when moving from GPT-5.6 to GPT-6 Astra.** Brad's established method uses defined scope, repository context, versioned SOPs, verification criteria, durable notes, and clear handoffs. The prior-generation guidance and his earlier methods articles provide the reference point; his testing and daily use provide the firsthand account. The aggregate records describe Astra activity and intervention. They do not establish a matched comparative failure rate or the underlying cause.

This directory contains **real, reviewed, de-identified aggregates**, released by Brad for public review under the repository's MIT license. It is separate from the synthetic kit examples and from participant submissions. All source projects retain generic labels, all observers are generic, and days are relative. No raw transcripts, source identities, identity hashes, private locators, mappings, or joins to named projects are included.

## Start here

- [Canonical evidence JSON](evidence.json), in [observational evidence format 1.0](../../docs/observational-evidence-format.md).
- [Methods, definitions, interpretation and limits](methodology.md).
- [Public source references](sources.md), including seven earlier methods articles and selected supporting and contrary replies.
- [Evidence reader](reader/README.md): interactive explorer and SVG/PNG figures.
- [Article and social drafts](https://github.com/DigitalMeld/digitalmeld.io/tree/main/docs/drafts/2026-09-09-astra-field-study): maintained in the digitalmeld.io repository.

## What the record contains

| Evidence layer | Frozen-window observation | What it does not establish |
|---|---:|---|
| Recorded usage | 25,254 responses; 557 turns | Useful work, HTTP calls, account-wide completeness |
| Recorded tokens | 3,420,584,663 total; 3,348,480,640 cached input | Unique text or billed spend |
| Coded contributions | 538 substantive units; 147 C; 154 D; 91 both; 210 union | A model failure rate or CSAT |
| Correction episodes | 78, including 31 repeated episodes | Independent trials |
| Process/SOP context | 102 C units associated with 40 episodes | 102 individually proven violations |
| Repository activity | 410 in-window PR merges across 17 identifiable repositories | Astra authorship or verified outcomes |
| Net boundary diffs | 3,753 repository-qualified paths; +311,765 / −18,415 text lines | Cumulative touches or productivity |
| Direct ratings | Not collected | Historical ratings must not be inferred |

D means explicit dissatisfaction. C means corrective steering. Their overlap is counted once in the union. Native user-message items (488) and substantive contributions (538) have different definitions; the latter reconcile typed and voice material contextually.

Both proposed causal explanations remain **entirely untested hypotheses** from roughly four or five days of personal experience: shortcuts toward completion may displace constraints, and delegation may lose requirements. Efficiency can be beneficial when it preserves the intended outcome and constraints. The six-day record window and its token volume do not validate either explanation.

## Reproduce the local checks and reader data

From the repository root, with Python 3.10 or later and no additional Python dependencies:

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate_evidence.py evidence/brad-groux-six-days-v1/evidence.json --ready
python3 tools/build_evidence_reader.py evidence/brad-groux-six-days-v1/evidence.json --out /tmp/astra-reader-preview.json
```

The last command creates a new file and refuses to overwrite one by default. To intentionally refresh the checked-in derived reader dataset:

```sh
python3 tools/build_evidence_reader.py evidence/brad-groux-six-days-v1/evidence.json --out evidence/brad-groux-six-days-v1/reader/explorer-data.json --replace
```

The reader JSON is a derivative, not a second independent source. Its numbers reconcile with the canonical JSON. The viewer performs no uploads and uses locally retained, MIT-licensed Three.js r186. See the [reader instructions](reader/README.md) for local HTTP preview. Publishing these files in Git does not deploy a website or publish a social post. Article and social drafts are maintained separately in digitalmeld.io.

## What would change the interpretation

A matched prospective model comparison, frozen instructions, independently reviewed task acceptance, traced delegation context, and independent coding would provide stronger evidence. Ordinary work, successful adherence, and contradictory experiences are welcome. Start with the repository's [contribution guidance](../../CONTRIBUTING.md); do not submit raw history.

Version 1 is a frozen observational snapshot. A correction should receive a new evidence version with a public aggregate-level change note. Existing private provenance remains private; no source-identity hashes are needed in a public revision history.
