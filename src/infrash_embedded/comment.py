#!/usr/bin/env python3
"""
Script to add energy optimization comments to source code files based on deep analysis results.
"""

import os
import re
import sys
import argparse
import json
from collections import defaultdict

class EnergyIssue:
    """Class representing an energy optimization issue."""
    def __init__(self, file_path, line_number, issue_type, description, suggestion, impact, optimization_gain):
        self.file_path = file_path
        self.line_number = line_number
        self.issue_type = issue_type
        self.description = description
        self.suggestion = suggestion
        self.impact = impact
        self.optimization_gain = optimization_gain

    def get_comment(self):
        """Generate a comment for this issue."""
        return f"// ENERGY: {self.description} - {self.suggestion} (Impact: {self.impact:.2f}, Gain: {self.optimization_gain:.2f})"


def parse_analysis_results(analysis_output):
    """Parse the analysis output to extract energy issues."""
    issues = []

    # Extract detailed issues section
    detailed_issues_match = re.search(r'=== Detailed Issues ===\s*(.*?)(?:===|\Z)', analysis_output, re.DOTALL)
    if not detailed_issues_match:
        print("Could not find detailed issues section in analysis output.")
        return issues

    detailed_issues_text = detailed_issues_match.group(1)

    # Regular expression to match issue entries
    issue_pattern = re.compile(
        r'(\d+)\.\s+([^:]+):(\d+)\s+-\s+([^\n]+)\s+'
        r'Type:\s+([^\n]+)\s+'
        r'Impact:\s+([\d.]+),\s+Optimization\s+gain:\s+([\d.]+)\s+'
        r'Suggestion:\s+([^\n]+)',
        re.DOTALL
    )

    for match in issue_pattern.finditer(detailed_issues_text):
        _, file_path, line_number, description, issue_type, impact, opt_gain, suggestion = match.groups()

        # Clean up file path to be relative to project root
        if file_path.startswith('/home/tom/github/zlecenia/maski/Programator_2025/'):
            file_path = file_path[len('/home/tom/github/zlecenia/maski/Programator_2025/'):]

        issues.append(EnergyIssue(
            file_path=file_path,
            line_number=int(line_number),
            issue_type=issue_type.strip(),
            description=description.strip(),
            suggestion=suggestion.strip(),
            impact=float(impact),
            optimization_gain=float(opt_gain)
        ))

    return issues


def add_comments_to_file(file_path, issues, backup=True, comment_format="inline", dry_run=False):
    """Add energy optimization comments to a file."""
    # Filter issues for this file
    file_issues = [issue for issue in issues if issue.file_path == file_path]
    if not file_issues:
        return 0

    # Sort issues by line number in descending order to avoid shifting line numbers
    file_issues.sort(key=lambda x: x.line_number, reverse=True)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0

    # Create backup if requested and not in dry run mode
    if backup and not dry_run:
        backup_path = file_path + '.bak'
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Created backup file: {backup_path}")
        except Exception as e:
            print(f"Error creating backup file for {file_path}: {e}")
            return 0

    comments_added = 0
    for issue in file_issues:
        # Check line number is valid
        if 0 <= issue.line_number - 1 < len(lines):
            comment = issue.get_comment()

            if comment_format == "inline":
                # Add comment to the end of the line
                line = lines[issue.line_number - 1].rstrip('\r\n')
                lines[issue.line_number - 1] = line + " " + comment + "\n"
            else:  # todo format
                # Insert comment on its own line before the code
                comment = "// TODO: ENERGY OPTIMIZATION: " + comment[10:]  # Replace "// ENERGY: " with "// TODO: ENERGY OPTIMIZATION: "
                lines.insert(issue.line_number - 1, comment + "\n")

                # Adjust line numbers for subsequent issues in the same file
                for other_issue in file_issues:
                    if other_issue != issue and other_issue.line_number > issue.line_number:
                        other_issue.line_number += 1

            comments_added += 1

    # Write changes if not in dry run mode
    if not dry_run and comments_added > 0:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Added {comments_added} comments to {file_path}")
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return 0
    else:
        print(f"Would add {comments_added} comments to {file_path}")

    return comments_added


def generate_markdown_report(issues, project_path, files_modified, comments_added):
    """Generate a markdown report of the issues and actions taken."""
    issues_by_file = defaultdict(list)
    for issue in issues:
        issues_by_file[issue.file_path].append(issue)

    report = [
        "# Energy Optimization Comments Report",
        "",
        f"## Project: {project_path}",
        "",
        f"Total issues addressed: {len(issues)}",
        f"Files modified: {files_modified}",
        f"Comments added: {comments_added}",
        "",
        "## Issues by File",
        ""
    ]

    # Sort files by the highest impact issue they contain
    sorted_files = sorted(issues_by_file.items(),
                          key=lambda x: max(issue.impact for issue in x[1]),
                          reverse=True)

    for file_path, file_issues in sorted_files:
        # Create a link to the file
        report.append(f"### [{file_path}]({file_path})")
        report.append("")
        report.append("| Line | Type | Description | Suggestion | Impact | Gain |")
        report.append("|------|------|-------------|------------|--------|------|")

        # Sort issues by line number
        for issue in sorted(file_issues, key=lambda x: x.line_number):
            report.append(f"| [{issue.line_number}]({file_path}#L{issue.line_number}) | {issue.issue_type} | {issue.description} | {issue.suggestion} | {issue.impact:.2f} | {issue.optimization_gain:.2f} |")

        report.append("")

    # Add recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. Focus on high-impact issues first (impact > 0.7)")
    report.append("2. Address busy-wait patterns with interrupt-driven approaches")
    report.append("3. Disable unused peripherals and clocks")
    report.append("4. Move loop-invariant operations outside loops")
    report.append("5. Use appropriate low power modes (LPM) when CPU is idle")

    return "\n".join(report)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Add energy optimization comments to source code files")
    parser.add_argument('project_path', help='Path to the project')
    parser.add_argument('analysis_file', help='File containing analysis results')
    parser.add_argument('--output', '-o', help='Output file for the report')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backup files')
    parser.add_argument('--format', choices=['inline', 'todo'], default='inline',
                        help='Comment format (inline or TODO style)')
    parser.add_argument('--min-impact', type=float, default=0.0, help='Minimum impact threshold (0.0 - 1.0)')

    args = parser.parse_args()

    # Read analysis results
    try:
        with open(args.analysis_file, 'r', encoding='utf-8') as f:
            analysis_output = f.read()
    except Exception as e:
        print(f"Error reading analysis file: {e}")
        return 1

    # Parse issues
    issues = parse_analysis_results(analysis_output)
    print(f"Found {len(issues)} issues in analysis results")

    # Filter issues by impact if requested
    if args.min_impact > 0:
        issues = [issue for issue in issues if issue.impact >= args.min_impact]
        print(f"Filtered to {len(issues)} issues with impact >= {args.min_impact}")

    # Process each file
    files_processed = set()
    total_comments_added = 0
    files_modified = 0

    for issue in issues:
        full_path = os.path.join(args.project_path, issue.file_path)

        # Skip files we've already processed
        if full_path in files_processed:
            continue

        files_processed.add(full_path)

        # Check if file exists
        if not os.path.isfile(full_path):
            print(f"Warning: File {full_path} does not exist, skipping")
            continue

        # Add comments to the file
        comments_added = add_comments_to_file(
            full_path,
            [i for i in issues if i.file_path == issue.file_path],
            backup=not args.no_backup,
            comment_format=args.format,
            dry_run=args.dry_run
        )

        total_comments_added += comments_added
        if comments_added > 0:
            files_modified += 1

    # Generate report
    report = generate_markdown_report(issues, args.project_path, files_modified, total_comments_added)

    # Write report to file if requested
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report written to {args.output}")
        except Exception as e:
            print(f"Error writing report: {e}")
    else:
        print("\n" + report)

    print(f"\nSummary: Added {total_comments_added} comments to {files_modified} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())