#!/usr/bin/env python3
"""
Convenience script to run the energy-optimizer tool without installing it.

This is useful during development.
"""

import os
import sys
import argparse

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Option 1: Use the CLI interface
from infrash_embedded.cli import main

# Option 2: Use the direct API
# from infrash_embedded import analyze_code
#
# def main():
#     issues = analyze_code('../../zlecenia/maski/Programator_2025')
#     for issue in issues:
#         print(f"{issue} - {issue.suggestion}")

if __name__ == "__main__":
    main()