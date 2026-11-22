#!/usr/bin/env python3
"""Compatibility command for scan_secrets.py. Usage: scan_context_secrets.py [ROOT]

Run me when: an existing command or script calls scan_context_secrets.py.
"""
import sys

from scan_secrets import main


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
