import argparse
import os
import sys
import logging
from typing import Dict, List, Any
import colorama
from colorama import Fore, Style
import optimization
import deep_analyzer
import analyzer


def deep_analyze_command(args):
    """Handle the 'deep-analyze' command."""
    print(f"{Fore.BLUE}Performing deep energy analysis on project: {args.project_path}{Style.RESET_ALL}")

    # Import the deep analyzer module
    from .deep_analyzer import deep_analyze_code, generate_optimization_summary

    # Setup configuration from command line arguments
    config = {
        'cross_file_analysis': not args.no_cross_file,
        'pattern_detection': not args.no_patterns,
        'mcu_specific': args.mcu_type.lower() if args.mcu_type else True,
        'find_fix_examples': not args.no_fix_examples
    }

    # Perform deep analysis
    result = deep_analyze_code(args.project_path, config)

    # Output results
    total_issues = len(result.issues)
    if total_issues > 0:
        print(f"\n{Fore.GREEN}Found {total_issues} energy optimization issues:{Style.RESET_ALL}")

        # Show issues by type
        print(f"\n{Fore.CYAN}Issues by type:{Style.RESET_ALL}")
        for issue_type, count in result.issue_types.items():
            print(f"- {issue_type}: {count} issues")

        # Show detected patterns if any
        if result.patterns:
            print(f"\n{Fore.CYAN}Detected energy patterns:{Style.RESET_ALL}")
            for pattern, occurrences in result.patterns.items():
                print(f"- {pattern}: {len(occurrences)} occurrences")

        # Show cross-file issues if any
        if result.cross_file_issues:
            print(f"\n{Fore.CYAN}Cross-file issues:{Style.RESET_ALL}")
            for issue, related_files in result.cross_file_issues:
                print(f"- {issue.description} in {issue.location.file}:{issue.location.line}")
                print(f"  Related files: {', '.join(related_files)}")

        # Show top high-impact issues
        high_impact_issues = [i for i in result.issues if i.impact >= 0.7]
        if high_impact_issues:
            print(f"\n{Fore.YELLOW}Top high-impact issues:{Style.RESET_ALL}")
            for i, issue in enumerate(sorted(high_impact_issues,
                                             key=lambda x: x.impact, reverse=True)[:5], 1):
                print(f"{i}. {issue.location.file}:{issue.location.line} - {issue.description}")
                print(f"   Impact: {issue.impact:.2f}, Optimization gain: {issue.optimization_gain:.2f}")
                print(f"   Suggestion: {issue.suggestion}")

        # Generate optimization summary
        summary = generate_optimization_summary(result)
        print(f"\n{Fore.GREEN}Optimization Summary:{Style.RESET_ALL}")
        print(f"Total energy impact: {summary['total_energy_impact']:.2f}")
        print(f"Potential optimization gain: {summary['total_optimization_gain']:.2f} ({summary['total_optimization_gain']*100:.1f}%)")

        # Generate detailed report if requested
        if args.report:
            report_content = _generate_deep_analysis_report(result, args.project_path)

            # Write report to file if output is specified
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report_content)
                print(f"{Fore.GREEN}Detailed report written to {args.output}{Style.RESET_ALL}")
            else:
                print("\n" + report_content)
    else:
        print(f"{Fore.GREEN}No energy issues found.{Style.RESET_ALL}")


def _generate_deep_analysis_report(result, project_path):
    """Generate a detailed report from deep analysis results."""
    report_lines = [
        "===== Deep Energy Analysis Report =====",
        f"Project: {project_path}",
        f"Total issues found: {len(result.issues)}",
        f"Files analyzed: {result.analyzed_files}",
        f"Total energy impact: {result.total_energy_impact:.2f}",
        f"Total optimization gain: {result.total_optimization_gain:.2f} ({result.total_optimization_gain*100:.1f}%)",
        "\n=== Issue Types ===",
    ]

    # Add issue types
    for issue_type, count in result.issue_types.items():
        report_lines.append(f"- {issue_type}: {count} issues")

    # Add detected patterns
    if result.patterns:
        report_lines.append("\n=== Detected Energy Patterns ===")
        for pattern, occurrences in result.patterns.items():
            report_lines.append(f"- {pattern}: {len(occurrences)} occurrences")

    # Add cross-file issues
    if result.cross_file_issues:
        report_lines.append("\n=== Cross-file Issues ===")
        for issue, related_files in result.cross_file_issues:
            report_lines.append(f"- {issue.description} in {issue.location.file}:{issue.location.line}")
            report_lines.append(f"  Related files: {', '.join(related_files)}")

    # Add detailed issues
    report_lines.append("\n=== Detailed Issues ===")
    for i, issue in enumerate(sorted(result.issues, key=lambda x: x.impact, reverse=True), 1):
        report_lines.append(f"\n{i}. {issue.location.file}:{issue.location.line} - {issue.description}")
        report_lines.append(f"   Type: {issue.issue_type}")
        report_lines.append(f"   Impact: {issue.impact:.2f}, Optimization gain: {issue.optimization_gain:.2f}")
        report_lines.append(f"   Suggestion: {issue.suggestion}")

        if issue.technical_details:
            report_lines.append(f"   Technical details: {issue.technical_details}")

        if issue.fix_example:
            report_lines.append(f"   Fix example:\n{issue.fix_example}")

        if issue.references:
            report_lines.append(f"   References: {', '.join(issue.references)}")

    # Add recommendations
    report_lines.append("\n=== Recommendations ===")
    report_lines.append("1. Focus on high-impact issues first, especially those with high optimization gain.")
    report_lines.append("2. Address cross-file issues to ensure consistent energy management across the codebase.")
    report_lines.append("3. Review power mode usage and ensure proper peripheral management.")
    report_lines.append("4. Replace busy-wait and polling patterns with interrupt-driven approaches.")
    report_lines.append("5. Use appropriate low power modes when the CPU is idle.")

    return "\n".join(report_lines)

def analyze_command(args):
    """Handle the 'analyze' command."""
    print(f"{Fore.BLUE}Analyzing project: {args.project_path}{Style.RESET_ALL}")

    analyzer = CodeAnalyzer(args.project_path)
    issues = analyzer.analyze()

    if issues:
        print(f"\n{Fore.GREEN}Found {len(issues)} potential energy issues:{Style.RESET_ALL}")
        for i, issue in enumerate(issues, 1):
            print(f"{Fore.YELLOW}{i}. {issue}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}No energy issues found.{Style.RESET_ALL}")

    if args.report:
        report_generator = ReportGenerator(args.project_path, issues)
        report = report_generator.generate_report(format_type="text")

        # Write report to file if output is specified
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"{Fore.GREEN}Report written to {args.output}{Style.RESET_ALL}")
        else:
            print("\n" + report)


def optimize_command(args):
    """Handle the 'optimize' command."""
    print(f"{Fore.BLUE}Optimizing project: {args.project_path}{Style.RESET_ALL}")

    # First analyze to find issues
    analyzer = CodeAnalyzer(args.project_path)
    issues = analyzer.analyze()

    if not issues:
        print(f"{Fore.GREEN}No energy issues found. Nothing to optimize.{Style.RESET_ALL}")
        return

    # Then optimize based on found issues
    optimizer = CodeOptimizer(args.project_path, issues)
    results = optimizer.optimize()

    # Display results
    print(f"\n{Fore.GREEN}Optimization Results:{Style.RESET_ALL}")
    print(f"  Fixed {results['fixed_issues']} out of {len(issues)} issues")
    print(f"  Estimated energy reduction: {results['estimated_energy_reduction']*100:.1f}%")
    print(f"  Modified {len(results['modified_files'])} files")

    if args.report:
        report_generator = ReportGenerator(args.project_path, issues, results)
        report_format = "markdown" if args.output and args.output.endswith('.md') else "text"
        report = report_generator.generate_report(format_type=report_format)

        # Write report to file if output is specified
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"{Fore.GREEN}Report written to {args.output}{Style.RESET_ALL}")
        else:
            print("\n" + report)


def report_command(args):
    """Handle the 'report' command."""
    print(f"{Fore.BLUE}Generating report for project: {args.project_path}{Style.RESET_ALL}")

    # First analyze to find issues
    analyzer = CodeAnalyzer(args.project_path)
    issues = analyzer.analyze()

    # Determine report format
    if args.format:
        report_format = args.format
    elif args.output and args.output.endswith('.md'):
        report_format = "markdown"
    else:
        report_format = "text"

    # Generate the report
    report_generator = ReportGenerator(args.project_path, issues)
    report = report_generator.generate_report(format_type=report_format)

    # Write report to file if output is specified
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"{Fore.GREEN}Report written to {args.output}{Style.RESET_ALL}")
    else:
        print("\n" + report)


def deploy_command(args):
    """Handle the 'deploy' command."""
    print(f"{Fore.BLUE}Deploying project: {args.project_path} to {args.server}{Style.RESET_ALL}")

    deployer = Deployer(args.project_path, args.server)
    success = deployer.deploy()

    if success:
        print(f"{Fore.GREEN}Deployment successful!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Deployment failed.{Style.RESET_ALL}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Energy Optimizer - A tool for analyzing and optimizing energy consumption in embedded systems.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Increase verbosity (can be used multiple times)')

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # 'analyze' command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze code for energy inefficiencies')
    analyze_parser.add_argument('project_path', help='Path to the project to analyze')
    analyze_parser.add_argument('--report', '-r', action='store_true', help='Generate a report')
    analyze_parser.add_argument('--output', '-o', help='Output file for report')
    analyze_parser.set_defaults(func=analyze_command)

    # 'deep-analyze' command
    deep_analyze_parser = subparsers.add_parser('deep-analyze',
                                                help='Perform deep energy analysis including cross-file issues and patterns')
    deep_analyze_parser.add_argument('project_path', help='Path to the project to analyze')
    deep_analyze_parser.add_argument('--report', '-r', action='store_true', help='Generate a detailed report')
    deep_analyze_parser.add_argument('--output', '-o', help='Output file for report')
    deep_analyze_parser.add_argument('--no-cross-file', action='store_true', help='Disable cross-file analysis')
    deep_analyze_parser.add_argument('--no-patterns', action='store_true', help='Disable pattern detection')
    deep_analyze_parser.add_argument('--no-fix-examples', action='store_true', help='Disable generation of fix examples')
    deep_analyze_parser.add_argument('--mcu-type', choices=['msp430', 'arm', 'avr', 'pic', 'generic'],
                                     help='Microcontroller type for specific optimizations')
    deep_analyze_parser.set_defaults(func=deep_analyze_command)

    # 'optimize' command
    optimize_parser = subparsers.add_parser('optimize', help='Optimize code for energy efficiency')
    optimize_parser.add_argument('project_path', help='Path to the project to optimize')
    optimize_parser.add_argument('--report', '-r', action='store_true', help='Generate a report')
    optimize_parser.add_argument('--output', '-o', help='Output file for report')
    optimize_parser.set_defaults(func=optimize_command)

    # 'report' command
    report_parser = subparsers.add_parser('report', help='Generate a report on energy efficiency')
    report_parser.add_argument('project_path', help='Path to the project to report on')
    report_parser.add_argument('--format', '-f', choices=['text', 'markdown', 'html', 'json'],
                               help='Report format')
    report_parser.add_argument('--output', '-o', help='Output file for report')
    report_parser.set_defaults(func=report_command)

    # 'comment' command - new command to add energy comments to source files
    comment_parser = subparsers.add_parser('comment', help='Add energy optimization comments to source files')
    comment_parser.add_argument('project_path', help='Path to the project to comment')
    comment_parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    comment_parser.add_argument('--no-backup', action='store_true', help='Skip creating backup files')
    comment_parser.add_argument('--format', choices=['inline', 'todo'], default='inline',
                                help='Comment format (inline or TODO style)')
    comment_parser.set_defaults(func=comment_command)

    # 'deploy' command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy optimized code')
    deploy_parser.add_argument('project_path', help='Path to the project to deploy')
    deploy_parser.add_argument('server', help='Server to deploy to (e.g., git@github.com:user/repo.git)')
    deploy_parser.set_defaults(func=deploy_command)

    # Parse arguments
    args = parser.parse_args()

    # Set verbosity level
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)

    # Execute command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)#!/usr/bin/env python3
