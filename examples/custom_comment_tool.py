#!/usr/bin/env python3
"""
Custom energy comment tool for adding energy optimization suggestions to source code files.
Based on results from deep_analyze_code function, this script adds comments to lines with energy issues.
"""

import os
import sys
import argparse
from typing import Dict, List, Any

# Add parent directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import necessary components
from infrash_embedded.deep_analyzer import deep_analyze_code, DeepEnergyIssue

def add_comments_to_file(file_path: str, issues: List[DeepEnergyIssue],
                         backup: bool = True, comment_format: str = "inline", dry_run: bool = False) -> int:
    """Add energy optimization comments to a file."""
    if not os.path.isfile(file_path):
        print(f"Warning: File {file_path} does not exist")
        return 0

    # Sort issues by line number in descending order to avoid shifting line numbers
    file_issues = sorted(issues, key=lambda x: x.location.line, reverse=True)

    # Skip if no issues for this file
    if not file_issues:
        return 0

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

    # Add comments to file
    comments_added = 0
    for issue in file_issues:
        line_num = issue.location.line - 1  # Convert to 0-based indexing
        if 0 <= line_num < len(lines):
            # Create comment text
            if comment_format == "inline":
                comment = f" // ENERGY: {issue.description} - {issue.suggestion}"
                if hasattr(issue, 'optimization_gain'):
                    comment += f" (Impact: {issue.impact:.2f}, Gain: {issue.optimization_gain:.2f})"

                # Add comment to the end of the line
                line = lines[line_num].rstrip('\r\n')
                lines[line_num] = line + comment + "\n"
            else:  # todo format
                comment = f"// TODO ENERGY: {issue.description} - {issue.suggestion}"
                if hasattr(issue, 'optimization_gain'):
                    comment += f" (Impact: {issue.impact:.2f}, Gain: {issue.optimization_gain:.2f})"
                comment += "\n"

                # Insert comment on a new line before the code
                lines.insert(line_num, comment)

                # Adjust line numbers for remaining issues
                for other_issue in file_issues:
                    if other_issue != issue and other_issue.location.line > issue.location.line:
                        other_issue.location.line += 1

            comments_added += 1

    # Write changes back to file
    if not dry_run and comments_added > 0:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Added {comments_added} comments to {file_path}")
        except Exception as e:
            print(f"Error writing to file {file_path}: {e}")
            return 0
    elif dry_run and comments_added > 0:
        print(f"Would add {comments_added} comments to {file_path}")

    return comments_added

def process_project(project_path: str, min_impact: float = 0.0,
                    comment_format: str = "inline", backup: bool = True,
                    dry_run: bool = False) -> Dict[str, Any]:
    """Process an entire project, analyzing and commenting files."""
    print(f"Analyzing project: {project_path}")

    # Run analysis
    config = {
        'cross_file_analysis': True,
        'pattern_detection': True,
        'mcu_specific': True,
        'find_fix_examples': True
    }

    result = deep_analyze_code(project_path, config)
    issues = result.issues

    print(f"Analysis complete. Found {len(issues)} issues.")

    # Filter issues by impact if threshold is set
    if min_impact > 0:
        filtered_issues = [issue for issue in issues if issue.impact >= min_impact]
        print(f"Filtered to {len(filtered_issues)} issues with impact >= {min_impact}")
    else:
        filtered_issues = issues

    # Group issues by file for processing
    files_to_process = {}
    for issue in filtered_issues:
        file_path = os.path.join(project_path, issue.location.file)
        if file_path not in files_to_process:
            files_to_process[file_path] = []
        files_to_process[file_path].append(issue)

    # Process each file
    total_comments = 0
    modified_files = 0

    for file_path, file_issues in files_to_process.items():
        comments_added = add_comments_to_file(
            file_path,
            file_issues,
            backup=backup,
            comment_format=comment_format,
            dry_run=dry_run
        )

        if comments_added > 0:
            modified_files += 1
            total_comments += comments_added

    # Generate summary
    summary = {
        "total_issues": len(issues),
        "filtered_issues": len(filtered_issues),
        "files_processed": len(files_to_process),
        "files_modified": modified_files,
        "comments_added": total_comments
    }

    # Print summary
    print("\nSummary:")
    print(f"Total issues found: {summary['total_issues']}")
    print(f"Issues matching impact threshold: {summary['filtered_issues']}")
    print(f"Files processed: {summary['files_processed']}")
    print(f"Files modified: {summary['files_modified']}")
    print(f"Comments added: {summary['comments_added']}")

    return summary

def main():
    """Main function to run the tool."""
    parser = argparse.ArgumentParser(
        description="Add energy optimization comments to source code based on deep analysis"
    )
    parser.add_argument('project_path', help='Path to the project to analyze and comment')
    parser.add_argument('--min-impact', type=float, default=0.7,
                        help='Minimum impact threshold (0.0-1.0) for comments')
    parser.add_argument('--format', choices=['inline', 'todo'], default='inline',
                        help='Comment format (inline or TODO style)')
    parser.add_argument('--no-backup', action='store_true',
                        help='Skip creating backup files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be changed without modifying files')

    args = parser.parse_args()

    process_project(
        args.project_path,
        min_impact=args.min_impact,
        comment_format=args.format,
        backup=not args.no_backup,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()