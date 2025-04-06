import re
import os
import sys
import logging
import argparse

# Add these imports to your cli.py
import os
import re
from typing import Dict, List, Any
from filter import FileFilter, create_default_filter
from typing import Dict, List, Any
import colorama
from colorama import Fore, Style

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from optimization import EnergyIssue, CodeOptimizer, Deployer, CodeAnalyzer, ReportGenerator
# Import the deep analyzer module
from deep_analyzer import deep_analyze_code, generate_optimization_summary
from _version import __version__

# Setup global logger (add this near the beginning of the file, with other imports)
logger = logging.getLogger("energy-optimizer.cli")



def deep_analyze_command(args):
    """Handle the 'deep-analyze' command."""
    print(f"{Fore.BLUE}Performing deep energy analysis on project: {args.project_path}{Style.RESET_ALL}")


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


# Add these parameters to your comment_parser or similar function
def comment_command(args):
    """Handle the 'comment' command - add energy optimization comments to source files."""
    print(f"{Fore.BLUE}Adding energy optimization comments to project: {args.project_path}{Style.RESET_ALL}")

    try:
        # Create file filter with command line options
        # Use create_custom_filter instead of create_default_filter
        file_filter = create_custom_filter(
            exclude_patterns=args.exclude_patterns,
            include_only_extensions=args.include_extensions,
            exclude_directories=args.exclude_dirs
        )
    except TypeError:
        # Fallback if the function doesn't accept those parameters
        logger.debug("Falling back to basic FileFilter initialization")
        file_filter = FileFilter(
            exclude_patterns=DEFAULT_EXCLUDE_PATTERNS,
            include_only_extensions=args.include_extensions,
            exclude_directories=args.exclude_dirs or DEFAULT_EXCLUDE_DIRS
        )

    # First analyze to find issues
    analyzer = CodeAnalyzer(args.project_path)
    issues = analyzer.analyze()

    # Alternatively, use deep analysis for more precise results
    if args.deep_analysis:
        config = {
            'cross_file_analysis': True,
            'pattern_detection': True,
            'mcu_specific': args.mcu_type.lower() if args.mcu_type else 'msp430',
            'find_fix_examples': True
        }
        result = deep_analyze_code(args.project_path, config)
        issues = result.issues

    if not issues:
        print(f"{Fore.GREEN}No energy issues found. Nothing to comment.{Style.RESET_ALL}")
        return

    # Count of files that would be modified
    modified_files = set()
    comment_count = 0

    # Filter issues by impact if threshold is set
    if hasattr(args, 'min_impact') and args.min_impact > 0:
        issues = [issue for issue in issues if
                  (hasattr(issue, 'impact') and issue.impact >= args.min_impact)]
        print(f"Filtered to {len(issues)} issues with impact >= {args.min_impact}")

    # Group issues by file
    issues_by_file = {}
    for issue in issues:
        file_path = getattr(issue, 'file', None)
        if file_path is None and hasattr(issue, 'location'):
            file_path = issue.location.file

        if file_path:
            full_path = os.path.join(args.project_path, file_path)

            # Skip filtered files - check if file should be excluded
            if hasattr(file_filter, 'should_exclude'):
                if file_filter.should_exclude(full_path):
                    logger.debug(f"Skipping filtered file: {full_path}")
                    continue
            # Filter by extension directly if the filter doesn't have should_exclude
            elif hasattr(file_filter, 'include_only_extensions') and file_filter.include_only_extensions:
                _, ext = os.path.splitext(full_path)
                if ext.lower() not in file_filter.include_only_extensions:
                    logger.debug(f"Skipping file with excluded extension: {full_path}")
                    continue

            if full_path not in issues_by_file:
                issues_by_file[full_path] = []
            issues_by_file[full_path].append(issue)
            modified_files.add(full_path)
            comment_count += 1

    # Display what would be done in dry-run mode
    if args.dry_run:
        print(f"\n{Fore.YELLOW}Dry run mode - no changes will be made{Style.RESET_ALL}")
        print(f"Would add {comment_count} comments to {len(modified_files)} files")
        for file_path in sorted(modified_files):
            relative_path = os.path.relpath(file_path, args.project_path)
            file_issues = issues_by_file[file_path]
            print(f"  {relative_path}: {len(file_issues)} comments")
        return

    # Make the actual changes
    files_modified = 0
    comments_added = 0

    for file_path, file_issues in issues_by_file.items():
        relative_path = os.path.relpath(file_path, args.project_path)

        # Read the file content
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            logger.error(f"Error reading file {relative_path}: {e}")
            continue

        # Create backup if not disabled
        if not args.no_backup:
            backup_path = file_path + '.bak'
            try:
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                logger.debug(f"Created backup file: {backup_path}")
            except Exception as e:
                logger.error(f"Error creating backup file for {relative_path}: {e}")
                continue

        # Add comments to the file
        modified = False
        file_comments_added = 0

        for issue in file_issues:
            # Get line number, handling different issue types
            line_num = issue.line if hasattr(issue, 'line') else issue.location.line

            if 0 <= line_num - 1 < len(lines):
                # Get fix example if available
                fix_example = ""
                if hasattr(issue, 'fix_example') and issue.fix_example:
                    fix_example = issue.fix_example
                elif hasattr(issue, 'suggestion') and issue.suggestion:
                    # Create more specific suggestion based on issue type and line content
                    fix_example = generate_fix_suggestion(issue, lines[line_num - 1])

                # Create the comment text based on format preference
                if args.format == 'inline':
                    # Generate more specific inline comment
                    comment = generate_inline_comment(issue, lines[line_num - 1])

                    # Add comment to the end of the line
                    line = lines[line_num - 1].rstrip('\r\n')
                    if "//" in line:  # if there's already a comment
                        parts = line.split("//", 1)
                        lines[line_num - 1] = parts[0] + "// " + comment + "\n"
                    else:
                        lines[line_num - 1] = line + " // " + comment + "\n"
                else:  # 'todo' format
                    # Generate more detailed multi-line comment
                    comment = generate_todo_comment(issue, lines[line_num - 1], fix_example)

                    # Insert comment on its own line before the code
                    lines.insert(line_num - 1, comment)

                    # Adjust line numbers for subsequent issues in the same file
                    for i in file_issues:
                        i_line = i.line if hasattr(i, 'line') else i.location.line
                        if i != issue and i_line > line_num:
                            if hasattr(i, 'line'):
                                i.line += 1
                            else:
                                i.location.line += 1

                modified = True
                file_comments_added += 1
                logger.debug(f"Added comment at {relative_path}:{line_num}")

        # Write back the modified file if changes were made
        if modified:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                files_modified += 1
                comments_added += file_comments_added
                logger.info(f"Modified file: {relative_path}")
            except Exception as e:
                logger.error(f"Error writing file {relative_path}: {e}")

    print(f"\n{Fore.GREEN}Added {comments_added} energy optimization comments to {files_modified} files{Style.RESET_ALL}")
    if not args.no_backup:
        print(f"Backup files created with '.bak' extension")

    # Generate report if requested
    if args.report:
        report_path = args.output if args.output else "energy_optimization_report.md"
        generate_energy_report(args.project_path, issues, files_modified, comments_added, report_path)
        print(f"{Fore.GREEN}Energy optimization report written to {report_path}{Style.RESET_ALL}")



# Add these command line arguments to your parser
def add_file_filter_args(parser):
    """Add file filtering arguments to the parser."""
    group = parser.add_argument_group('File filtering options')
    group.add_argument('--include-extensions', nargs='+', default=['.c', '.h', '.cpp', '.hpp'],
                       help='Only include files with these extensions (e.g., .c .h)')
    group.add_argument('--exclude-dirs', nargs='+',
                       help='Exclude directories (e.g., build test)')
    group.add_argument('--exclude-patterns', nargs='+',
                       help='Additional regex patterns for files to exclude (e.g., ".*_test\\.c$")')
    return parser


def generate_inline_comment(issue, line):
    """Generate a more specific inline comment based on the issue type and code context."""
    desc = issue.description if hasattr(issue, 'description') else "Energy issue detected"
    suggestion = issue.suggestion if hasattr(issue, 'suggestion') else ""
    impact = issue.impact if hasattr(issue, 'impact') else 0.0
    gain = issue.optimization_gain if hasattr(issue, 'optimization_gain') else 0.0

    # Start with basic comment
    comment = f"ENERGY: {desc}"

    # Add more specific information based on issue type and code context
    issue_type = issue.issue_type if hasattr(issue, 'issue_type') else ""

    if "busy_wait" in issue_type or "busy_wait_pattern" in issue_type:
        if "while (1)" in line or "while(1)" in line:
            comment += f" - {suggestion} (zastąp pętlą: _BIS_SR(LPM3_bits + GIE); // CPU śpi, przerwania wybudzają)"
        elif "for" in line and "delay" in line.lower():
            comment += f" - {suggestion} (użyj Timer_A z przerwaniem zamiast aktywnego oczekiwania)"
        else:
            comment += f" - {suggestion} (użyj _BIS_SR(LPM3_bits + GIE))"

    elif "suboptimal_sleep_mode" in issue_type:
        if "LPM0" in line:
            comment += f" - {suggestion} (zastosuj _BIS_SR(LPM3_bits) zamiast LPM0 dla dłuższych okresów bezczynności)"
        else:
            comment += f" - {suggestion} (zastosuj głębszy tryb uśpienia)"

    elif "loop" in issue_type and ("unnecessary" in issue_type or "inefficient" in issue_type):
        invariant_op = find_invariant_operation(line)
        if invariant_op:
            comment += f" - {suggestion} (przenieś operację '{invariant_op}' przed pętlę)"
        else:
            comment += f" - {suggestion} (przenieś niezmienne obliczenia poza pętlę)"

    elif "adc" in issue_type.lower() or "suboptimal_adc" in issue_type:
        if "ADC12CTL0 =" in line or "ADC12CTL0 |=" in line:
            comment += f" - {suggestion} (użyj ADC12SHT_0 dla krótszego czasu próbkowania gdy to możliwe)"
        else:
            comment += f" - {suggestion} (zoptymalizuj konfigurację ADC)"

    elif "peripheral_not_disabled" in issue_type:
        peripheral_type = detect_peripheral_type(line)
        comment += f" - {suggestion} (wyłącz {peripheral_type} po użyciu: {peripheral_type}_disable())"

    elif "clock" in issue_type.lower():
        if "BCSCTL" in line or "DCOCTL" in line:
            comment += f" - {suggestion} (obniż częstotliwość zegara gdy nie jest potrzebna wysoka wydajność)"
        else:
            comment += f" - {suggestion} (wyłącz nieużywane zegary)"

    elif "pin" in issue_type or "port" in issue_type or "gpio" in issue_type:
        if "OUT" in line and "DIR" not in line:
            comment += f" - {suggestion} (najpierw skonfiguruj kierunek PIN_DIR, potem ustaw wartość PIN_OUT)"
        else:
            comment += f" - {suggestion} (popraw konfigurację portów GPIO)"

    elif impact >= 0.7:  # Wysokie znaczenie
        comment += f" - {suggestion} (Impact: {impact:.2f}, Szacowane oszczędności: {gain*100:.0f}%)"
    else:
        comment += f" - {suggestion}"

    return comment


def generate_todo_comment(issue, line, fix_example=""):
    """Generate a detailed TODO comment with specific fix suggestions based on code context."""
    desc = issue.description if hasattr(issue, 'description') else "Energy issue detected"
    suggestion = issue.suggestion if hasattr(issue, 'suggestion') else ""
    impact = issue.impact if hasattr(issue, 'impact') else 0.0
    gain = issue.optimization_gain if hasattr(issue, 'optimization_gain') else 0.0
    issue_type = issue.issue_type if hasattr(issue, 'issue_type') else ""

    comment = f"// TODO ENERGY OPTIMIZATION: {desc}\n"

    # Add context-specific suggestions
    if "busy_wait" in issue_type or "busy_wait_pattern" in issue_type:
        if "while (1)" in line or "while(1)" in line:
            comment += f"// Zalecenie: {suggestion}\n"
            comment += "// Użyj trybu niskiego poboru mocy z przerwaniami zamiast aktywnego oczekiwania:\n"
            comment += "// _BIS_SR(LPM3_bits + GIE); // CPU śpi, przerwania wybudzają\n"
        elif "for" in line and "delay" in line.lower():
            comment += f"// Zalecenie: {suggestion}\n"
            comment += "// Użyj Timer_A z przerwaniem zamiast aktywnego oczekiwania:\n"
            comment += "// TA0CCR0 = 1000; // Ustaw timer\n"
            comment += "// TA0CCTL0 = CCIE; // Włącz przerwanie\n"
            comment += "// TA0CTL = TASSEL_2 + MC_1 + ID_3; // Uruchom timer\n"
            comment += "// _BIS_SR(LPM3_bits + GIE); // CPU śpi, timer wybudzi przez przerwanie\n"
        else:
            comment += f"// Zalecenie: {suggestion}\n"

    elif "adc" in issue_type.lower():
        comment += f"// Zalecenie: {suggestion}\n"
        comment += "// Optymalizuj konfigurację ADC dla oszczędności energii:\n"
        comment += "// ADC12CTL0 = ADC12SHT_0 + ADC12ON; // Najkrótszy czas próbkowania\n"
        comment += "// ADC12CTL1 = ADC12SHP; // Timer próbkowania\n"
        comment += "// ADC12CTL2 = ADC12RES_1; // 10-bit dla mniejszego zużycia energii gdy wystarczy\n"

    elif "peripheral_not_disabled" in issue_type:
        peripheral_type = detect_peripheral_type(line)
        comment += f"// Zalecenie: {suggestion}\n"
        comment += f"// Wyłącz {peripheral_type} po użyciu, aby zmniejszyć zużycie energii:\n"
        if "UART" in peripheral_type or "UCA" in peripheral_type:
            comment += "// UCA0CTL1 |= UCSWRST; // Reset modułu UART\n"
            comment += "// UCA0IE &= ~(UCRXIE + UCTXIE); // Wyłącz przerwania UART\n"
        elif "SPI" in peripheral_type or "UCB" in peripheral_type:
            comment += "// UCB0CTL1 |= UCSWRST; // Reset modułu SPI\n"
        elif "ADC" in peripheral_type:
            comment += "// ADC12CTL0 &= ~ADC12ON; // Wyłącz ADC\n"
        elif "Timer" in peripheral_type:
            comment += "// TA0CTL &= ~MC_3; // Zatrzymaj timer\n"

    elif "clock" in issue_type.lower():
        comment += f"// Zalecenie: {suggestion}\n"
        comment += "// Dostosuj częstotliwość zegara do wymagań:\n"
        comment += "// if (!high_performance_needed) {\n"
        comment += "//   BCSCTL1 = CALBC1_1MHZ; // Użyj 1MHz zamiast wyższych częstotliwości\n"
        comment += "//   DCOCTL = CALDCO_1MHZ;\n"
        comment += "// }\n"

    # Add technical details if available
    if hasattr(issue, 'technical_details') and issue.technical_details:
        comment += f"// Szczegóły techniczne: {issue.technical_details}\n"

    # Add impact and potential gain
    if impact > 0 or gain > 0:
        comment += f"// Wpływ: {impact:.2f}, Potencjalne oszczędności energii: {gain*100:.1f}%\n"

    # Add custom fix example if provided or use the default one
    if fix_example:
        comment += f"// Przykład poprawki:\n// {fix_example}\n"

    # Add references if available
    if hasattr(issue, 'references') and issue.references:
        comment += f"// Referencje: {', '.join(issue.references)}\n"

    return comment


def generate_fix_suggestion(issue, line):
    """Generate more specific fix suggestion based on issue type and line of code."""
    issue_type = issue.issue_type if hasattr(issue, 'issue_type') else ""

    if "busy_wait" in issue_type or "polling" in issue_type:
        if "while" in line and ("1" in line or "true" in line.lower()):
            return "Zastąp aktywne oczekiwanie trybem LPM z przerwaniami:\n// /* Przygotuj obsługę przerwania */\n// __bis_SR_register(LPM3_bits + GIE); // Przejdź w tryb LPM3 z włączonymi przerwaniami"
        elif "for" in line and "delay" in line.lower():
            return "Zastąp pętlę opóźniającą timerem z przerwaniem:\n// TA0CCR0 = 1000; // Ustaw timer\n// TA0CCTL0 = CCIE; // Włącz przerwanie\n// TA0CTL = TASSEL_2 + MC_1; // Uruchom timer\n// __bis_SR_register(LPM3_bits + GIE); // Przejdź w tryb LPM3, timer wybudzi przez przerwanie"
        else:
            return "Zamień aktywne oczekiwanie na tryb LPM z przerwaniami:\n// __bis_SR_register(LPM3_bits + GIE); // Użyj trybu LPM3 z włączonymi przerwaniami"

    elif "sleep_mode" in issue_type:
        if "LPM0" in line:
            return "Zastosuj głębszy tryb uśpienia:\n// __bis_SR_register(LPM3_bits); // Użyj LPM3 zamiast LPM0 dla znaczących oszczędności energii"
        else:
            return "Zastosuj głębszy tryb uśpienia:\n// __bis_SR_register(LPM3_bits); // LPM3 zużywa znacząco mniej energii niż LPM0/LPM1"

    elif "loop" in issue_type and ("unnecessary" in issue_type or "inefficient" in issue_type):
        invariant = find_invariant_operation(line)
        if invariant:
            return f"Przenieś niezmienne operacje poza pętlę:\n// {invariant} = obliczenie(); // Oblicz raz przed pętlą\n// for(...) {{ użyj {invariant} zamiast powtarzać obliczenia }}"
        else:
            return "Przenieś niezmienne operacje i obliczenia poza pętlę:\n// wynik = obliczenie(); // Oblicz raz przed pętlę\n// for(i=0; i<n; i++) { użyj 'wynik' }"

    elif "peripheral_not_disabled" in issue_type:
        peripheral = detect_peripheral_type(line)
        if "UART" in peripheral or "UCA" in peripheral:
            return f"Po zakończeniu użytkowania {peripheral}:\n// UCA0CTL1 |= UCSWRST; // Zresetuj {peripheral}\n// UCA0IE &= ~(UCRXIE + UCTXIE); // Wyłącz przerwania {peripheral}"
        elif "SPI" in peripheral or "UCB" in peripheral:
            return f"Po zakończeniu użytkowania {peripheral}:\n// UCB0CTL1 |= UCSWRST; // Zresetuj {peripheral}\n// UCB0IE &= ~UCRXIE; // Wyłącz przerwania {peripheral}"
        elif "ADC" in peripheral:
            return f"Po zakończeniu użytkowania {peripheral}:\n// ADC12CTL0 &= ~ADC12ON; // Wyłącz {peripheral} gdy nie jest używane"
        elif "Timer" in peripheral:
            return f"Po zakończeniu użytkowania {peripheral}:\n// TA0CTL &= ~MC_3; // Zatrzymaj {peripheral}\n// TA0IE &= ~TAIE; // Wyłącz przerwania {peripheral}"
        else:
            return f"Po zakończeniu użytkowania {peripheral}:\n// {peripheral}_disable(); // Wyłącz {peripheral} gdy nie jest używane"

    elif "adc" in issue_type.lower() or "suboptimal_adc" in issue_type:
        return "Zoptymalizuj konfigurację ADC dla oszczędności energii:\n// ADC12CTL0 = ADC12SHT_0 + ADC12ON; // Użyj najkrótszego czasu próbkowania gdy pozwala na to sygnał\n// ADC12CTL2 = ADC12RES_1; // Użyj 10-bit rozdzielczości gdy wystarczy"

    elif "clock" in issue_type:
        if "BCSCTL" in line or "DCOCTL" in line:
            return "Dostosuj częstotliwość zegara do potrzeb:\n// if (!high_performance_needed) {\n//   BCSCTL1 = CALBC1_1MHZ; // Użyj niższej częstotliwości gdy to możliwe\n//   DCOCTL = CALDCO_1MHZ;\n// }"
        else:
            return "Wyłącz nieużywane zegary:\n// BCSCTL2 &= ~SELS; // Wyłącz nieużywane źródło zegara\n// BCSCTL3 |= LFXT1S_0; // Wyłącz oscylator kryształu gdy nie jest potrzebny"

    elif "pin" in issue_type or "port" in issue_type or "gpio" in issue_type:
        return "Poprawnie skonfiguruj piny GPIO:\n// P1DIR |= BIT0; // Najpierw ustaw kierunek\n// P1OUT |= BIT0; // Potem ustaw wartość\n// P1REN |= BIT1; // Włącz rezystor podciągający/ściągający dla wejść"

    else:
        return issue.suggestion if hasattr(issue, 'suggestion') else "Zoptymalizuj ten fragment kodu pod kątem zużycia energii"


def find_invariant_operation(line):
    """Try to identify potential loop-invariant operations in the code line."""
    # Przykładowa prosta implementacja - w prawdziwym systemie
    # należałoby zastosować analizę syntaktyczną kodu
    potential_invariants = []

    # Szukaj wywołań funkcji, które mogą być niezmienne
    function_match = re.search(r'(\w+)\s*\([^)]*\)', line)
    if function_match:
        potential_invariants.append(function_match.group(1))

    # Szukaj przypisań, które mogą być niezmienne
    assignment_match = re.search(r'(\w+)\s*=\s*[^;]+', line)
    if assignment_match:
        potential_invariants.append(assignment_match.group(1))

    if potential_invariants:
        return potential_invariants[0]
    return "zmienna"


def detect_peripheral_type(line):
    """Detect the peripheral type from the code line."""
    if re.search(r'U[CS]A\d|UART', line, re.IGNORECASE):
        return "UART"
    elif re.search(r'UCB\d|SPI', line, re.IGNORECASE):
        return "SPI"
    elif re.search(r'ADC', line, re.IGNORECASE):
        return "ADC"
    elif re.search(r'TA\d|TB\d|Timer', line, re.IGNORECASE):
        return "Timer"
    elif re.search(r'P\d(OUT|DIR|REN)', line):
        return "GPIO"
    else:
        return "peryferia"


def generate_energy_report(project_path, issues, files_modified, comments_added, report_path):
    """Generate a detailed report of energy issues and optimizations."""
    # Grupuj problemy według plików
    issues_by_file = {}
    for issue in issues:
        file_path = issue.file if hasattr(issue, 'file') else issue.location.file
        if file_path not in issues_by_file:
            issues_by_file[file_path] = []
        issues_by_file[file_path].append(issue)

    # Grupuj problemy według typu
    issues_by_type = {}
    for issue in issues:
        issue_type = issue.issue_type if hasattr(issue, 'issue_type') else "unknown"
        if issue_type not in issues_by_type:
            issues_by_type[issue_type] = []
        issues_by_type[issue_type].append(issue)

    # Generuj raport w formacie Markdown
    report = [
        "# Raport optymalizacji energetycznej",
        "",
        f"## Projekt: {project_path}",
        "",
        f"**Znalezione problemy:** {len(issues)}",
        f"**Zmodyfikowane pliki:** {files_modified}",
        f"**Dodane komentarze:** {comments_added}",
        "",
        "## Podsumowanie według typu problemu",
        ""
    ]

    # Tabela podsumowująca typy problemów
    report.append("| Typ problemu | Liczba wystąpień | Średni wpływ | Średni potencjalny zysk |")
    report.append("|--------------|-----------------|-------------|-------------------------|")

    for issue_type, type_issues in sorted(issues_by_type.items(), key=lambda x: len(x[1]), reverse=True):
        avg_impact = sum(i.impact if hasattr(i, 'impact') else 0 for i in type_issues) / len(type_issues)
        avg_gain = sum(i.optimization_gain if hasattr(i, 'optimization_gain') else 0 for i in type_issues) / len(type_issues)

        report.append(f"| {issue_type} | {len(type_issues)} | {avg_impact:.2f} | {avg_gain:.2f} |")

    # Szczegóły według plików
    report.append("")
    report.append("## Szczegóły według plików")
    report.append("")

    for file_path, file_issues in sorted(issues_by_file.items()):
        report.append(f"### {file_path}")
        report.append("")
        report.append("| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |")
        report.append("|-------|-------------|------|----------|-------|------|")

        for issue in sorted(file_issues, key=lambda x: x.line if hasattr(x, 'line') else x.location.line):
            line_num = issue.line if hasattr(issue, 'line') else issue.location.line
            issue_type = issue.issue_type if hasattr(issue, 'issue_type') else ""
            description = issue.description if hasattr(issue, 'description') else ""
            suggestion = issue.suggestion if hasattr(issue, 'suggestion') else ""
            impact = issue.impact if hasattr(issue, 'impact') else 0
            gain = issue.optimization_gain if hasattr(issue, 'optimization_gain') else 0

            report.append(f"| {line_num} | {issue_type} | {description} | {suggestion} | {impact:.2f} | {gain:.2f} |")

        report.append("")

    # Rekomendacje
    report.append("## Rekomendacje")
    report.append("")
    report.append("1. **Priorytety optymalizacji**: Skup się najpierw na problemach o wysokim wpływie (> 0.7).")
    report.append("2. **Busy-wait i polling**: Zastąp aktywne oczekiwanie podejściem opartym na przerwaniach.")
    report.append("3. **Tryby uśpienia**: Wykorzystuj głębsze tryby uśpienia (LPM3/LPM4) zamiast LPM0.")
    report.append("4. **Zarządzanie peryferiami**: Wyłączaj nieużywane peryferia i zegary.")
    report.append("5. **Optymalizacja pętli**: Przenoś niezmienne operacje poza pętle.")

    # Zapisz raport do pliku
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
    except Exception as e:
        logger.error(f"Error writing report to {report_path}: {e}")


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
    # Add file filtering to analyze command
    add_file_filter_args(analyze_parser)
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
    # Add file filtering to deep-analyze command
    add_file_filter_args(deep_analyze_parser)
    deep_analyze_parser.set_defaults(func=deep_analyze_command)

    # 'optimize' command
    optimize_parser = subparsers.add_parser('optimize', help='Optimize code for energy efficiency')
    optimize_parser.add_argument('project_path', help='Path to the project to optimize')
    optimize_parser.add_argument('--report', '-r', action='store_true', help='Generate a report')
    optimize_parser.add_argument('--output', '-o', help='Output file for report')
    # Add file filtering to optimize command
    add_file_filter_args(optimize_parser)
    optimize_parser.set_defaults(func=optimize_command)

    # 'report' command
    report_parser = subparsers.add_parser('report', help='Generate a report on energy efficiency')
    report_parser.add_argument('project_path', help='Path to the project to report on')
    report_parser.add_argument('--format', '-f', choices=['text', 'markdown', 'html', 'json'],
                               help='Report format')
    report_parser.add_argument('--output', '-o', help='Output file for report')
    report_parser.set_defaults(func=report_command)

    # 'comment' command - enhanced version to add energy comments to source files
    comment_parser = subparsers.add_parser('comment', help='Add energy optimization comments to source files')
    comment_parser.add_argument('project_path', help='Path to the project to comment')
    comment_parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    comment_parser.add_argument('--no-backup', action='store_true', help='Skip creating backup files')
    comment_parser.add_argument('--format', choices=['inline', 'todo'], default='inline',
                                help='Comment format (inline or TODO style)')
    comment_parser.add_argument('--min-impact', type=float, default=0.0, help='Only comment issues with impact >= threshold (0.0-1.0)')
    comment_parser.add_argument('--deep-analysis', action='store_true', help='Use deep analysis for more detailed comments')
    comment_parser.add_argument('--mcu-type', choices=['msp430', 'arm', 'avr', 'pic', 'generic'], default='msp430',
                                help='Microcontroller type for specific optimizations')
    comment_parser.add_argument('--report', '-r', action='store_true', help='Generate a detailed report')
    comment_parser.add_argument('--output', '-o', help='Output file for report (default: energy_optimization_report.md)')
    # Add file filtering to comment command
    add_file_filter_args(comment_parser)
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
