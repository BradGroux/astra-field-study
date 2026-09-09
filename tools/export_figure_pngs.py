#!/usr/bin/env python3
"""Optional PNG export using an existing ImageMagick and a local Roboto TTF."""
import argparse
from pathlib import Path
import shutil
import subprocess
from build_articles import FIGURES, READER


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font',type=Path,required=True,help='Path to a locally available Roboto .ttf file.')
    args=parser.parse_args()
    executable=shutil.which('magick')
    if not executable or not args.font.is_file():
        parser.error('An existing ImageMagick installation and local Roboto TTF are required. SVGs need neither.')
    for name in FIGURES:
        subprocess.run([executable,'-font',str(args.font.resolve()),str(READER/'figures'/f'{name}.svg'),str(READER/'figures'/f'{name}.png')],check=True)
    print('Exported six PNGs. Inspect each output before sharing.')

if __name__=='__main__':main()
