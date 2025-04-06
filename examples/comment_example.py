#!/usr/bin/env python3
# examples/comment_example.py
"""
Example script demonstrating the code commenting capability of the energy optimizer tool.
This script adds energy optimization suggestions as comments directly in source files.
"""

import os
import sys

# Add the parent directory to sys.path to make the package importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now import from the package
from infrash_embedded.cli import comment_command
from infrash_embedded.deep_analyzer import deep_analyze_code

def main():
    """Run a sample comment operation on a project directory."""
    # Use a sample project directory - replace with your actual project path
    project_path = os.path.join(os.path.dirname(__file__), '../../../zlecenia/maski/Programator_2025')

    # Create a mock args object to pass to the command
    class Args:
        def __init__(self):
            self.project_path = project_path
            self.dry_run = False               # Set to True to see what would be done without making changes
            self.no_backup = False             # Set to True to skip creating backup files
            self.format = 'inline'             # Comment format: 'inline' or 'todo'
            self.min_impact = 0.7              # Only comment issues with impact >= this threshold
            self.output = 'energy_report.md'   # Output file for the generated report

    args = Args()

    # Call the comment command
    print(f"Adding energy optimization comments to project: {project_path}")
    comment_command(args)

    # Alternative approach: analyze and comment manually
    print("\nAlternative approach - custom commenting process:")

    # First perform deep analysis
    config = {
        'cross_file_analysis': True,
        'pattern_detection': True,
        'mcu_specific': True,
        'find_fix_examples': True
    }
    result = deep_analyze_code(project_path, config)
    print(f"Analysis complete. Found {len(result.issues)} issues.")

    # Now manually process high-impact issues
    high_impact_issues = [issue for issue in result.issues if issue.impact >= 0.7]
    print(f"Processing {len(high_impact_issues)} high-impact issues...")

    # Count issues by type for reporting
    issue_types = {}
    for issue in high_impact_issues:
        if issue.issue_type not in issue_types:
            issue_types[issue.issue_type] = 0
        issue_types[issue.issue_type] += 1

    # Print summary of processed issues
    print("\nIssue types processed:")
    for issue_type, count in issue_types.items():
        print(f"- {issue_type}: {count} issues")

    print("\nComment operation complete.")

if __name__ == "__main__":
    main()