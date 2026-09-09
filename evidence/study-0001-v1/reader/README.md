# Evidence reader and figures

The [canonical evidence](../evidence.json), [methods](../methodology.md), [interactive explorer](explorer.html), and six [figures and captions](figure-captions.md) belong to Astra Field Study.

Read the published [study](https://go.sstb.ai/astra-study) and [companion blog](https://go.sstb.ai/astra-blog), or share the [repository](https://go.sstb.ai/astra-repo). The study links to the hosted explorer; the instructions below run the evidence reader locally.

Editorial source and social drafts live in [digitalmeld.io](https://github.com/DigitalMeld/digitalmeld.io/tree/main/docs/drafts/2026-09-09-astra-field-study). Do not add editorial drafts to this repository.

From this repository root, run `python3 tools/preview_reader.py`, then open http://127.0.0.1:8767/reader/explorer.html. All runtime files are local; no upload endpoint or CDN is used.

Day and project filters apply to usage and coded observations. Repository activity always covers the full window. The optional 3D profile shows one project across six days; exact values remain available in HTML. Missing repository data is not zero, and no reviewed contributions means no rate.

Regenerate SVGs with `python3 tools/build_figures.py`. Optional PNG export: `python3 tools/export_figure_pngs.py --font /absolute/path/to/Roboto.ttf`, using existing ImageMagick and a local Roboto TTF. Caption definitions live in `tools/figure_catalog.py`. See [rendering notes](../../../docs/reader-design.md).

Three.js remains under [MIT](vendor/LICENSE), with its [release record](vendor/release.json). Roboto uses the [SIL Open Font License](vendor/Roboto-OFL.txt) and [font notice](vendor/Roboto-NOTICE.md).
