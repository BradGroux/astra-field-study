# README output examples

Both images are rendered examples of real tool output from `examples/synthetic-submission.json`. They contain invented data only. They are not browser or spreadsheet screenshots.

- `terminal-preview.svg` / `.png`: complete `validate.preview()` output after validating the fixture.
- `csv-output.svg` / `.png`: the exact export recipe from `docs/local-results.md` is executed against the fixture in a disposable temporary directory. Its `usage.csv` is transposed for readability; no metrics are added.

Regenerate SVG sources from the repository root with `python3 tools/build_readme_examples.py`. This uses only the Python standard library, validates the fixture, reads no private history, and replaces only the two named SVG files. Regeneration does not publish anything.

The checked-in PNGs were rasterized from those SVG text elements with an existing Pillow installation and the local Menlo font. No dependency or font was added to the project. To refresh the PNGs, use an existing local SVG renderer that preserves whitespace and quotation marks. Inspect both complete images after rendering: some renderers drop JSON quotes or indentation. Check numbers against the fixture, CSV alignment, clipping, captions, and legibility. Do not replace these examples with real personal output.
