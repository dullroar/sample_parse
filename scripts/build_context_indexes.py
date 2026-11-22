#!/usr/bin/env python3
"""Compatibility command for build_indexes.py. Usage: build_context_indexes.py [--check] [ROOT]

Run me when: an existing command or script calls build_context_indexes.py.
"""
import sys

from build_indexes import main


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
