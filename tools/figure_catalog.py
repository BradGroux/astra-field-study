"""Public figure captions and export paths; no article content."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
READER=ROOT/"evidence/brad-groux-six-days-v1/reader"
FIGURES={
 'responses-by-day': ('Recorded responses by relative study day', '25,254 responses across six relative days. Day 6 ends at the common cutoff. Source: recorded usage in evidence.json.'),
 'steering-partition': ('Exclusive categories among 538 substantive contributions', 'Each square represents one contribution. The five categories are exclusive: 310 routine, 63 dissatisfaction only, 56 correction only, 91 both, and 18 ambiguous. Source: contextual review, protocol 1.1.'),
 'token-composition': ('Cached and uncached input tokens, with output shown separately', 'The strip divides input tokens into cached and uncached input. Output is shown separately and includes reasoning. Source: recorded usage in evidence.json.'),
 'day-project-matrix': ('Recorded response counts for six days and eighteen generic projects', 'Each cell reports an exact response count. The color scale is linear and fixed across all cells. Project numbers are generic labels. Source: recorded usage in evidence.json.'),
 'episode-outcomes': ('Recorded outcomes for 78 correction episodes', 'Fourteen episodes were confirmed resolved in the reviewed context. Forty-five had no established closure; their later status is unknown. Source: contextual review, protocol 1.1.'),
 'repository-merges': ('PR merges by generic project over the full study window', '410 in-window PR merges across 17 identifiable repositories. Counts include all authors and are not allocated to individual study days. Source: repository activity in evidence.json.'),
}
