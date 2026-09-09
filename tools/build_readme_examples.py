#!/usr/bin/env python3
"""Render README examples from synthetic data; standard-library SVG output only."""
import csv
from html import escape
import io
from pathlib import Path
import subprocess
import sys
import tempfile

from validate import load, preview, validate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/images'

def svg(name, title, subtitle, lines, footnote, width=1200):
    height = 150 + len(lines) * 27 + 65
    content = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
               f'<title>{escape(title)}</title>',
               '<rect width="100%" height="100%" fill="#111d2b"/>',
               f'<text x="40" y="52" fill="#f4b85b" font-family="DejaVu Sans" font-size="17">SYNTHETIC EXAMPLE · NOT PARTICIPANT FINDINGS</text>',
               f'<text x="40" y="94" fill="#edf2fa" font-family="DejaVu Sans" font-size="28">{escape(title)}</text>',
               f'<text x="40" y="125" fill="#a9b7c9" font-family="DejaVu Sans" font-size="17">{escape(subtitle)}</text>']
    for i, line in enumerate(lines):
        content.append(f'<text x="40" y="{165 + i * 27}" fill="#edf2fa" font-family="DejaVu Sans Mono" font-size="18" xml:space="preserve">{escape(line)}</text>')
    content.append(f'<text x="40" y="{height - 26}" fill="#a9b7c9" font-family="DejaVu Sans" font-size="16">{escape(footnote)}</text></svg>')
    (OUT / name).write_text('\n'.join(content) + '\n', encoding='utf-8')

def main():
    OUT.mkdir(exist_ok=True)
    data = validate(load(ROOT / 'examples/synthetic-submission.json'))
    summary = preview(data)
    svg('terminal-preview.svg', 'Validated terminal preview',
        'python3 tools/validate.py examples/synthetic-submission.json --preview',
        summary.splitlines(), 'Full synthetic summary. Consent shown here belongs only to the invented example.')
    # Execute the documented recipe against the synthetic fixture, not a second exporter.
    guide = (ROOT / 'docs/local-results.md').read_text()
    recipe = guide.split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
    with tempfile.TemporaryDirectory(prefix='astra-readme-') as temporary:
        target = Path(temporary) / 'view'
        subprocess.run([sys.executable, '-', str(ROOT / 'examples/synthetic-submission.json'), str(target)],
                       input=recipe, text=True, cwd=ROOT, check=True, capture_output=True)
        rows = list(csv.DictReader(io.StringIO((target / 'usage.csv').read_text())))
        assert [row['scope'] for row in rows] == ['window', 'day']
        lines = [f'{"FIELD":<36} {"WINDOW":>12} {"DAY 1":>12}', '─' * 64]
        for field in rows[0]:
            lines.append(f'{field:<36} {rows[0][field] or "—":>12} {rows[1][field] or "—":>12}')
        svg('csv-output.svg', 'Your local usage.csv export',
            'Actual documented export, transposed here so every field is readable.', lines,
            'Window and day are separate scopes. Do not add the window row to the daily rows.')
    print('Rendered two synthetic SVG examples in docs/images. No private data read.')

if __name__ == '__main__':
    main()
