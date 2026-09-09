#!/usr/bin/env python3
"""Validate and canonicalize an aggregate draft; never scrub raw Codex history."""
import argparse
import json
from pathlib import Path
import sys
from validate import load, validate, ValidationError

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('draft',type=Path)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    try:
        data=validate(load(a.draft),ready=True)
        with a.out.open('x',encoding='utf-8') as f:
            f.write(json.dumps(data,indent=2,sort_keys=True)+'\n')
        print('Canonical aggregate written. Review the exact file and Git diff before submission. Nothing uploaded.')
    except (ValidationError,OSError,RecursionError):
        print('Rejected. Only reviewed, consented allowlisted aggregates can be copied; raw history cannot be sanitized here.',file=sys.stderr)
        return 1
    return 0
if __name__=='__main__':
    sys.exit(main())
