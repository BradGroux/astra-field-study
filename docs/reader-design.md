# Evidence reader rendering

Article and social drafts belong to [digitalmeld.io](https://github.com/DigitalMeld/digitalmeld.io/tree/main/docs/drafts/2026-09-09-astra-field-study). This repository maintains the evidence explorer and figures. Use Roboto and the dark reader palette. Review chart wording and numeric label spacing with the rendered figures.

## Figure sources and choices

`tools/build_figures.py` validates the public evidence JSON before producing six desktop and six mobile SVGs. SVGs embed the licensed local Roboto font. No private source records are needed.

| Figure | Form | Question and denominator |
| --- | --- | --- |
| Responses by day | Columns starting at zero | How do 25,254 recorded responses divide across six days? Day 6 is partial. |
| Reviewed contributions | Waffle, one square per contribution | How do 538 contributions divide into five exclusive categories? |
| Token composition | Input composition plus separate output total | How much input was cached? Output is outside the input denominator. |
| Day/project counts | Matrix with exact counts | When was each project active? The linear color scale is shared by all 108 cells. |
| Correction outcomes | Horizontal bars starting at zero | What was recorded for 78 episodes? An unknown outcome is not a confirmed failure. |
| Repository merges | Ranked dots starting at zero | How do 410 merges divide among 17 repositories? All authors and the full window are included. |

The optional 3D view shows six days for one selected project. It uses a fixed maximum across projects and keeps exact values available in HTML. Repository totals are never narrowed by the day filter. An unresolved repository remains missing data; a selection with no reviewed contributions has no correction rate.

## Local checks

From the repository root:

```sh
python3 tools/build_figures.py
python3 -m unittest discover -s tests
python3 tools/preview_reader.py
```

For PNG exports, use an existing ImageMagick installation and a local Roboto TTF:

```sh
python3 tools/export_figure_pngs.py --font /absolute/path/to/Roboto.ttf
```

The PNG export does not install software or download fonts. Review every PNG and SVG after changes; the renderers handle font metrics differently. Check long titles, numeric labels, contrast, and spacing at both layouts. In the reader, check source links, image loading, keyboard filters, missing-data selections and the optional 3D camera. Rebuilding files is not visual verification.
