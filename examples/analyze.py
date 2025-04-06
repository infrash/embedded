#!/usr/bin/env python3
"""
Example script to analyze a specific project for energy inefficiencies.
"""

import os
import sys
import argparse

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from infrash_embedded import analyze_code

# Replace this with the path to your actual project
PROJECT_PATH = "../../zlecenia/maski/Programator_2025"

def main():
    # Check if the project path exists
    if not os.path.exists(PROJECT_PATH):
        print(f"Project path not found: {PROJECT_PATH}")
        print("Please update the PROJECT_PATH variable in this script.")
        return

    print(f"Analyzing project: {PROJECT_PATH}")
    issues = analyze_code(PROJECT_PATH)

    if not issues:
        print("No energy issues found.")
        return

    print(f"\nFound {len(issues)} potential energy issues:")

    # Group issues by type
    issue_types = {}
    for issue in issues:
        if issue.issue_type not in issue_types:
            issue_types[issue.issue_type] = []
        issue_types[issue.issue_type].append(issue)

    # Print summary by issue type
    print("\nIssues by type:")
    for issue_type, type_issues in issue_types.items():
        print(f"- {issue_type}: {len(type_issues)} issues")

    # Print detailed information for each issue
    print("\nDetailed issues:")
    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. {issue}")
        print(f"   Type: {issue.issue_type}")
        print(f"   Impact: {issue.impact:.2f} (higher = more impact)")
        print(f"   Suggestion: {issue.suggestion}")


if __name__ == "__main__":
    main()