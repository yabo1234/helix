"""
Legacy wrapper for the Triple Helix Innovation Agent.

This repository originally contained this hyphenated filename, which is not
importable as a Python module. The actual tool entrypoint is implemented in
`triple_helix_innovation.py`.
"""

from __future__ import annotations

import sys

import triple_helix_innovation


def main() -> int:
    # Delegate to the real CLI wrapper for consistent behavior.
    return triple_helix_innovation._main(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
