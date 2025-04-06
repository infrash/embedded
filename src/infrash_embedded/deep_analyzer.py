#!/usr/bin/env python3
"""
Deep Energy Analysis Module

This module extends the basic analyzer with more advanced energy optimization techniques,
particularly focused on embedded systems and MSP430 microcontrollers.
"""

import os
import re
import sys
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from analyzer import (
    EnergyIssue,
    SourceLocation,
    analyze_code,
    CodeAnalysisManager
)
from _version import __version__

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("energy-optimizer.deep-analyzer")


class DeepEnergyIssue(EnergyIssue):
    """Extended energy issue with additional information for deep analysis."""

    def __init__(self,
                 issue_type: str,
                 location: SourceLocation,
                 description: str,
                 impact: float,
                 suggestion: str,
                 code_snippet: str = "",
                 optimization_gain: float = 0.0,
                 related_files: List[str] = None,
                 fix_example: str = "",
                 technical_details: str = "",
                 references: List[str] = None):
        super().__init__(issue_type, location, description, impact, suggestion, code_snippet)
        self.optimization_gain = optimization_gain  # Estimated energy savings in percentage
        self.related_files = related_files or []    # List of related files that might need changes
        self.fix_example = fix_example              # Example code showing how to fix the issue
        self.technical_details = technical_details  # Detailed technical explanation
        self.references = references or []          # Reference documents/links


class DeepAnalysisResult:
    """Result of a deep energy analysis on a project."""

    def __init__(self):
        self.issues: List[DeepEnergyIssue] = []
        self.issue_types: Dict[str, int] = defaultdict(int)
        self.file_issues: Dict[str, List[DeepEnergyIssue]] = defaultdict(list)
        self.total_energy_impact: float = 0.0
        self.total_optimization_gain: float = 0.0
        self.analyzed_files: int = 0
        self.total_files: int = 0
        self.patterns: Dict[str, List[Tuple[str, int]]] = defaultdict(list)  # Pattern -> [(file, line), ...]
        self.cross_file_issues: List[Tuple[DeepEnergyIssue, List[str]]] = []  # Issues that span multiple files

    def add_issue(self, issue: DeepEnergyIssue):
        """Add an issue to the analysis results."""
        self.issues.append(issue)
        self.issue_types[issue.issue_type] += 1
        self.file_issues[issue.location.file].append(issue)
        self.total_energy_impact += issue.impact
        self.total_optimization_gain += issue.optimization_gain

        if len(issue.related_files) > 0:
            self.cross_file_issues.append((issue, issue.related_files))

    def add_pattern(self, pattern_name: str, file_path: str, line_number: int):
        """Add a detected code pattern to the results."""
        self.patterns[pattern_name].append((file_path, line_number))

    def get_issues_by_type(self, issue_type: str) -> List[DeepEnergyIssue]:
        """Get all issues of a specific type."""
        return [issue for issue in self.issues if issue.issue_type == issue_type]

    def get_issues_by_file(self, file_path: str) -> List[DeepEnergyIssue]:
        """Get all issues for a specific file."""
        return self.file_issues.get(file_path, [])

    def get_high_impact_issues(self, threshold: float = 0.7) -> List[DeepEnergyIssue]:
        """Get issues with impact above the specified threshold."""
        return [issue for issue in self.issues if issue.impact >= threshold]


class DeepCodeAnalyzer:
    """Advanced code analyzer for detecting energy inefficiencies."""

    def __init__(self, project_path: str, config: Optional[Dict[str, Any]] = None):
        self.project_path = os.path.abspath(project_path)
        self.config = config or {}
        self.result = DeepAnalysisResult()
        self.code_manager = CodeAnalysisManager(project_path, config)

        # Configure deep analysis options
        self.cross_file_analysis = self.config.get('cross_file_analysis', True)
        self.pattern_detection = self.config.get('pattern_detection', True)
        self.mcu_specific = self.config.get('mcu_specific', True)
        self.find_fix_examples = self.config.get('find_fix_examples', True)

        # Initialize pattern databases
        self._init_pattern_databases()

    def _init_pattern_databases(self):
        """Initialize databases for pattern detection."""
        # Energy inefficiency patterns in embedded systems
        self.energy_patterns = {
            'busy_wait': re.compile(r'while\s*\(\s*1\s*\)|for\s*\([^;]*;[^;]*;[^)]*\)\s*;'),
            'delay_loop': re.compile(r'for\s*\(\s*\w+\s*=\s*0\s*;\s*\w+\s*<\s*[0-9]+\s*;\s*\w+\+\+\s*\)'),
            'high_freq_config': re.compile(r'(DCOCTL|BCSCTL|UCSCTL)\d*\s*=.*?(_16MHZ|_25MHZ|_20MHZ)'),
            'missing_lpm': re.compile(r'_BIS_SR\s*\(\s*[^L]'),
            'polling': re.compile(r'while\s*\(\s*!\s*\(\s*\w+\s*&\s*\w+\s*\)\s*\)'),
            'unconfigured_pins': re.compile(r'P\dOUT\s*[|&^]?=.*?(?![.\s\S]*?P\dDIR\s*[|&^]?=)'),
        }

        # MSP430 specific energy optimization patterns
        self.msp430_patterns = {
            'suboptimal_adc': re.compile(r'ADC(10|12)CTL0\s*[|]?=\s*(?!.*?ADC10SHT_0)'),
            'uart_no_lpm': re.compile(r'(UCA|UCB)\d(CTL1|IE)\s*[|]?=\s*UC(A|B)(\w+)(?![.\s\S]*?LPM[0-4])'),
            'high_power_mode': re.compile(r'LPM0(?![.\s\S]*?LPM[1-4])'),
            'unused_clock': re.compile(r'BCSCTL\d\s*[|]?=\s*(\w+).*?(?!.*?(BCSCTL\d.*?&=\s*~\1))'),
        }

        # Fix patterns to suggest improvements
        self.fix_patterns = {
            'busy_wait': "/* Replace busy wait with LPM mode */\n_BIS_SR(LPM0_bits + GIE); // Enter LPM0 with interrupts enabled",
            'delay_loop': "/* Replace delay loop with timer */\nTA0CCR0 = 1000; // Set timer\nTA0CTL = TASSEL_2 + MC_1 + TAIE; // Start timer\n_BIS_SR(LPM0_bits); // Enter LPM, timer will wake up",
            'high_freq_config': "/* Reduce clock frequency when high performance not needed */\nif (!high_performance_needed) {\n    BCSCTL1 = CALBC1_1MHZ; // Use 1MHz instead\n    DCOCTL = CALDCO_1MHZ;\n}",
            'missing_lpm': "/* Add low power mode */\n_BIS_SR(LPM3_bits + GIE); // Enter LPM3 with interrupts enabled",
            'polling': "/* Replace polling with interrupt-driven approach */\nIE1 |= SPECIFIC_INT_ENABLE; // Enable specific interrupt\n_BIS_SR(LPM0_bits + GIE); // Enter LPM, interrupt will wake up",
            'unconfigured_pins': "/* Configure pin direction before setting output */\nP1DIR |= BIT0; // Set pin as output\nP1OUT |= BIT0; // Then set the output value",
        }

        # MSP430 specific fix examples
        self.msp430_fixes = {
            'suboptimal_adc': "/* Optimize ADC sampling time */\nADC10CTL0 = ADC10SHT_0 + ADC10ON; // Use shortest sampling time when appropriate",
            'uart_no_lpm': "/* Enable LPM with UART interrupts */\nUCA0IE |= UCRXIE; // Enable UART receive interrupt\n_BIS_SR(LPM3_bits + GIE); // Enter LPM3, UART interrupt will wake up",
            'high_power_mode': "/* Use deeper sleep mode */\n_BIS_SR(LPM3_bits + GIE); // Use LPM3 instead of LPM0 to save more power",
            'unused_clock': "/* Disable unused clock */\nBCSCTL2 &= ~SPECIFIC_CLOCK_BITS; // Turn off clock when not needed",
        }

        # References for technical details
        self.references = {
            'msp430_lpm': "MSP430 Family Guide: Low-Power Modes",
            'efficient_code': "Embedded Systems: Introduction to Arm Cortex-M Microcontrollers (5th Ed)",
            'clock_management': "MSP430 User's Guide: Clock System",
            'peripheral_config': "MSP430x5xx Family User's Guide: Peripherals",
        }

    def analyze(self) -> DeepAnalysisResult:
        """Perform deep energy analysis on the project."""
        logger.info(f"Starting deep energy analysis of project at {self.project_path}")

        # First run the basic analyzer to get initial issues
        basic_issues = self.code_manager.analyze_project()
        self.result.analyzed_files = len(self.code_manager.context.file_cache)

        # Convert basic issues to deep issues with additional information
        for issue in basic_issues:
            deep_issue = self._enhance_issue(issue)
            self.result.add_issue(deep_issue)

        # Perform pattern-based detection if enabled
        if self.pattern_detection:
            self._detect_patterns()

        # Cross-file analysis if enabled
        if self.cross_file_analysis:
            self._perform_cross_file_analysis()

        logger.info(f"Deep analysis completed. Found {len(self.result.issues)} issues.")

        return self.result

    def _enhance_issue(self, issue: EnergyIssue) -> DeepEnergyIssue:
        """Enhance a basic energy issue with additional information."""
        # Start with the basic information
        file_path = issue.location.file
        deep_issue = DeepEnergyIssue(
            issue_type=issue.issue_type,
            location=issue.location,
            description=issue.description,
            impact=issue.impact,
            suggestion=issue.suggestion,
            code_snippet=issue.code_snippet,
        )

        # Add optimization gain estimate based on issue type
        if issue.issue_type == "peripheral_not_disabled":
            deep_issue.optimization_gain = 0.05  # 5% energy savings
            deep_issue.technical_details = "Disabling unused peripherals can significantly reduce power consumption."
            deep_issue.references = [self.references['peripheral_config']]

        elif issue.issue_type == "unused_clocks_enabled":
            deep_issue.optimization_gain = 0.10  # 10% energy savings
            deep_issue.technical_details = "Disabling unused clocks can reduce power consumption by 10-15%."
            deep_issue.references = [self.references['clock_management']]

        elif issue.issue_type == "inefficient_loop":
            deep_issue.optimization_gain = 0.03  # 3% energy savings
            deep_issue.technical_details = "Optimizing loops reduces CPU cycles and energy consumption."
            deep_issue.references = [self.references['efficient_code']]

        elif issue.issue_type == "unnecessary_loop_operations":
            deep_issue.optimization_gain = 0.02  # 2% energy savings
            deep_issue.technical_details = "Moving invariant operations outside loops reduces CPU cycles."

        elif issue.issue_type == "incomplete_port_config":
            deep_issue.optimization_gain = 0.01  # 1% energy savings
            deep_issue.technical_details = "Properly configured I/O ports reduce energy leakage."
            deep_issue.references = [self.references['peripheral_config']]

        # Add fix example if possible
        if self.find_fix_examples:
            deep_issue.fix_example = self._get_fix_example(issue)

        return deep_issue

    def _get_fix_example(self, issue: EnergyIssue) -> str:
        """Generate a code example showing how to fix the issue."""
        fix_example = ""

        # Default pattern-based fixes
        if issue.issue_type == "peripheral_not_disabled":
            if "UART" in issue.description:
                fix_example = "/* Disable UART when not in use */\nUCA0CTL1 |= UCSWRST; // Put UART in reset state\nUCA0IE &= ~(UCRXIE + UCTXIE); // Disable UART interrupts"
            elif "SPI" in issue.description:
                fix_example = "/* Disable SPI when not in use */\nUCB0CTL1 |= UCSWRST; // Put SPI in reset state\nUCB0IE &= ~UCRXIE; // Disable SPI interrupts"
            elif "Timer" in issue.description:
                fix_example = "/* Disable Timer when not in use */\nTA0CTL &= ~MC_3; // Stop timer\nTA0IE &= ~TAIE; // Disable timer interrupts"
            elif "GPIO" in issue.description:
                fix_example = "/* Configure unused GPIO pins to reduce power */\nP1DIR |= UNUSED_PINS; // Set as output\nP1OUT &= ~UNUSED_PINS; // Set to low state"
            elif "ADC" in issue.description:
                fix_example = "/* Disable ADC when not in use */\nADC10CTL0 &= ~ADC10ON; // Turn off ADC"

        elif issue.issue_type == "unused_clocks_enabled":
            fix_example = "/* Disable unused clocks */\nBCSCTL2 &= ~SELS; // Disable SMCLK source\n// OR\nBCSCTL3 |= LFXT1S_0; // Turn off crystal oscillator if not needed"

        elif issue.issue_type == "inefficient_loop":
            fix_example = "/* Optimize loop */\n// Instead of:\n// while(condition) { ... }\n\n// Pre-compute values outside the loop\nint precomputed = heavy_calculation();\nwhile(simple_condition) {\n    // Use precomputed value\n}"

        elif issue.issue_type == "unnecessary_loop_operations":
            fix_example = "/* Move loop-invariant operations outside */\n// Instead of:\n// for(i=0; i<n; i++) { x = costly_operation(); ... }\n\n// Do this:\nx = costly_operation(); // Pre-compute outside loop\nfor(i=0; i<n; i++) {\n    // Use pre-computed value\n}"

        elif issue.issue_type == "incomplete_port_config":
            fix_example = "/* Configure port direction before setting output */\nP1DIR |= BIT0; // First set as output\nP1OUT |= BIT0; // Then set output value"

        return fix_example

    def _detect_patterns(self):
        """Detect energy inefficiency patterns in the code."""
        logger.info("Performing pattern-based detection")

        for file_path, content in self.code_manager.context.file_cache.items():
            # Skip non-source files
            if not file_path.endswith(('.c', '.h', '.cpp', '.hpp')):
                continue

            file_lines = content.splitlines()
            relative_path = os.path.relpath(file_path, self.project_path)

            # Detect general energy patterns
            for pattern_name, pattern_regex in self.energy_patterns.items():
                for match in pattern_regex.finditer(content):
                    # Get line number for the match
                    line_number = content[:match.start()].count('\n') + 1
                    self.result.add_pattern(pattern_name, relative_path, line_number)

                    # Create a deep issue for this pattern
                    location = SourceLocation(file=relative_path, line=line_number)

                    # Get code snippet
                    start_line = max(0, line_number - 2)
                    end_line = min(len(file_lines), line_number + 3)
                    code_snippet = "\n".join(file_lines[start_line:end_line])

                    # Pattern-specific details
                    if pattern_name == 'busy_wait':
                        issue = DeepEnergyIssue(
                            issue_type="busy_wait_pattern",
                            location=location,
                            description="Busy-wait pattern detected - wastes energy by keeping CPU active",
                            impact=0.75,
                            suggestion="Replace busy-wait with low power mode and interrupts",
                            code_snippet=code_snippet,
                            optimization_gain=0.15,
                            fix_example=self.fix_patterns.get(pattern_name, ""),
                            technical_details="Busy-waiting keeps the CPU fully active, consuming maximum power.",
                            references=[self.references['msp430_lpm'], self.references['efficient_code']]
                        )
                    elif pattern_name == 'delay_loop':
                        issue = DeepEnergyIssue(
                            issue_type="delay_loop_pattern",
                            location=location,
                            description="Delay loop detected - inefficient way to create delays",
                            impact=0.65,
                            suggestion="Use timers instead of delay loops",
                            code_snippet=code_snippet,
                            optimization_gain=0.08,
                            fix_example=self.fix_patterns.get(pattern_name, ""),
                            technical_details="Delay loops keep the CPU active, whereas timer-based delays allow CPU to sleep.",
                            references=[self.references['efficient_code']]
                        )
                    elif pattern_name == 'high_freq_config':
                        issue = DeepEnergyIssue(
                            issue_type="high_frequency_pattern",
                            location=location,
                            description="High frequency clock configuration - may consume unnecessary power",
                            impact=0.60,
                            suggestion="Use lower frequency when high performance not needed",
                            code_snippet=code_snippet,
                            optimization_gain=0.20,
                            fix_example=self.fix_patterns.get(pattern_name, ""),
                            technical_details="Higher clock frequencies exponentially increase power consumption.",
                            references=[self.references['clock_management']]
                        )
                    elif pattern_name == 'missing_lpm':
                        issue = DeepEnergyIssue(
                            issue_type="missing_lpm_pattern",
                            location=location,
                            description="Missing low power mode - CPU stays in active mode",
                            impact=0.80,
                            suggestion="Use appropriate low power mode (LPM) when CPU is idle",
                            code_snippet=code_snippet,
                            optimization_gain=0.30,
                            fix_example=self.fix_patterns.get(pattern_name, ""),
                            technical_details="LPM3 can reduce power consumption by up to 30x compared to active mode.",
                            references=[self.references['msp430_lpm']]
                        )
                    elif pattern_name == 'polling':
                        issue = DeepEnergyIssue(
                            issue_type="polling_pattern",
                            location=location,
                            description="Polling pattern detected - keeps CPU active waiting for events",
                            impact=0.70,
                            suggestion="Use interrupt-driven approach instead of polling",
                            code_snippet=code_snippet,
                            optimization_gain=0.12,
                            fix_example=self.fix_patterns.get(pattern_name, ""),
                            technical_details="Polling keeps CPU active while waiting for events, interrupts allow CPU to sleep.",
                            references=[self.references['efficient_code']]
                        )
                    elif pattern_name == 'unconfigured_pins':
                        issue = DeepEnergyIssue(
                            issue_type="unconfigured_pins_pattern",
                            location=location,
                            description="Unconfigured GPIO pin directions",
                            impact=0.40,
                            suggestion="Configure pin directions explicitly",
                            code_snippet=code_snippet,
                            optimization_gain=0.01,
                            fix_example=self.fix_patterns.get(pattern_name, ""),
                            technical_details="Unconfigured pins can lead to floating inputs or contention.",
                            references=[self.references['peripheral_config']]
                        )
                    else:
                        # Generic pattern issue
                        issue = DeepEnergyIssue(
                            issue_type=f"{pattern_name}_pattern",
                            location=location,
                            description=f"{pattern_name.replace('_', ' ')} pattern detected",
                            impact=0.50,
                            suggestion=f"Consider optimizing the {pattern_name.replace('_', ' ')} pattern",
                            code_snippet=code_snippet,
                            optimization_gain=0.05
                        )

                    self.result.add_issue(issue)

            # MSP430-specific patterns if enabled
            if self.mcu_specific:
                for pattern_name, pattern_regex in self.msp430_patterns.items():
                    for match in pattern_regex.finditer(content):
                        # Get line number for the match
                        line_number = content[:match.start()].count('\n') + 1
                        self.result.add_pattern(pattern_name, relative_path, line_number)

                        # Create a deep issue for this pattern
                        location = SourceLocation(file=relative_path, line=line_number)

                        # Get code snippet
                        start_line = max(0, line_number - 2)
                        end_line = min(len(file_lines), line_number + 3)
                        code_snippet = "\n".join(file_lines[start_line:end_line])

                        # Pattern-specific details
                        if pattern_name == 'suboptimal_adc':
                            issue = DeepEnergyIssue(
                                issue_type="suboptimal_adc_pattern",
                                location=location,
                                description="Suboptimal ADC configuration detected",
                                impact=0.45,
                                suggestion="Optimize ADC sampling time when appropriate",
                                code_snippet=code_snippet,
                                optimization_gain=0.03,
                                fix_example=self.msp430_fixes.get(pattern_name, ""),
                                technical_details="Shorter ADC sampling times consume less energy when signal conditions allow.",
                                references=[self.references['peripheral_config']]
                            )
                        elif pattern_name == 'uart_no_lpm':
                            issue = DeepEnergyIssue(
                                issue_type="uart_no_lpm_pattern",
                                location=location,
                                description="UART configured without low power mode",
                                impact=0.55,
                                suggestion="Configure UART to work with low power modes",
                                code_snippet=code_snippet,
                                optimization_gain=0.07,
                                fix_example=self.msp430_fixes.get(pattern_name, ""),
                                technical_details="UART can operate in low power modes using interrupts to wake the CPU.",
                                references=[self.references['peripheral_config'], self.references['msp430_lpm']]
                            )
                        elif pattern_name == 'high_power_mode':
                            issue = DeepEnergyIssue(
                                issue_type="high_power_mode_pattern",
                                location=location,
                                description="Higher power mode used when deeper sleep possible",
                                impact=0.65,
                                suggestion="Use deeper sleep mode when possible (LPM3 or LPM4)",
                                code_snippet=code_snippet,
                                optimization_gain=0.15,
                                fix_example=self.msp430_fixes.get(pattern_name, ""),
                                technical_details="LPM3 and LPM4 provide significantly more power savings than LPM0 or LPM1.",
                                references=[self.references['msp430_lpm']]
                            )
                        elif pattern_name == 'unused_clock':
                            issue = DeepEnergyIssue(
                                issue_type="unused_clock_pattern",
                                location=location,
                                description="Clock enabled but appears unused",
                                impact=0.60,
                                suggestion="Disable unused clocks to save power",
                                code_snippet=code_snippet,
                                optimization_gain=0.10,
                                fix_example=self.msp430_fixes.get(pattern_name, ""),
                                technical_details="Clock oscillators consume significant power even when not being used by peripherals.",
                                references=[self.references['clock_management']]
                            )
                        else:
                            # Generic MSP430 pattern issue
                            issue = DeepEnergyIssue(
                                issue_type=f"{pattern_name}_pattern",
                                location=location,
                                description=f"{pattern_name.replace('_', ' ')} pattern detected in MSP430 code",
                                impact=0.50,
                                suggestion=f"Consider optimizing the {pattern_name.replace('_', ' ')} pattern",
                                code_snippet=code_snippet,
                                optimization_gain=0.05
                            )

                        self.result.add_issue(issue)

    def _perform_cross_file_analysis(self):
        """Analyze relationships between files for energy issues."""
        logger.info("Performing cross-file analysis")

        # Build file dependency graph
        file_dependencies = self._build_dependency_graph()

        # Check for sleep mode consistency across files
        self._check_sleep_mode_consistency(file_dependencies)

        # Check for clock configuration consistency
        self._check_clock_consistency(file_dependencies)

        # Check for peripheral management consistency
        self._check_peripheral_consistency(file_dependencies)

    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build a dependency graph of files in the project."""
        dependencies = defaultdict(list)

        # Simple include-based dependencies
        include_pattern = re.compile(r'#include\s+[<"]([^>"]+)[>"]')

        for file_path, content in self.code_manager.context.file_cache.items():
            if not file_path.endswith(('.c', '.h', '.cpp', '.hpp')):
                continue

            relative_path = os.path.relpath(file_path, self.project_path)

            # Find all includes
            for match in include_pattern.finditer(content):
                included_file = match.group(1)

                # Try to resolve the included file path
                resolved_path = self._resolve_include_path(included_file, file_path)
                if resolved_path:
                    dependencies[relative_path].append(resolved_path)

        return dependencies

    def _resolve_include_path(self, include_name: str, source_file: str) -> Optional[str]:
        """Resolve an include to an actual file path."""
        # First check if the include exists relative to the source file
        source_dir = os.path.dirname(source_file)
        candidate = os.path.normpath(os.path.join(source_dir, include_name))

        if os.path.exists(candidate):
            return os.path.relpath(candidate, self.project_path)

        # Check common include directories
        for include_dir in ['include', 'inc', 'lib', 'libs']:
            candidate = os.path.normpath(os.path.join(self.project_path, include_dir, include_name))
            if os.path.exists(candidate):
                return os.path.relpath(candidate, self.project_path)

        # Try direct path from project root
        candidate = os.path.normpath(os.path.join(self.project_path, include_name))
        if os.path.exists(candidate):
            return os.path.relpath(candidate, self.project_path)

        return None



    def _check_sleep_mode_consistency(self, dependencies: Dict[str, List[str]]):
        """Check for consistency in sleep mode usage across files."""
        # Find all LPM usage
        lpm_pattern = re.compile(r'_BIS_SR\s*\(\s*(LPM[0-4]_bits|LPM[0-4])')
        lpm_by_file = {}

        for file_path, content in self.code_manager.context.file_cache.items():
            if not file_path.endswith(('.c', '.h', '.cpp', '.hpp')):
                continue

            relative_path = os.path.relpath(file_path, self.project_path)
            file_lines = content.splitlines()

            for match in lpm_pattern.finditer(content):
                lpm_mode = match.group(1)
                line_number = content[:match.start()].count('\n') + 1

                if relative_path not in lpm_by_file:
                    lpm_by_file[relative_path] = []

                lpm_by_file[relative_path].append((lpm_mode, line_number))

        # Check for inconsistent LPM usage across dependent files
        for file_path, deps in dependencies.items():
            if file_path not in lpm_by_file:
                continue

            file_lpms = [mode for mode, _ in lpm_by_file[file_path]]

            for dep in deps:
                if dep in lpm_by_file:
                    dep_lpms = [mode for mode, _ in lpm_by_file[dep]]

                    # Check for inconsistent sleep modes
                    if file_lpms and dep_lpms and set(file_lpms) != set(dep_lpms):
                        # Find deepest and shallowest sleep modes
                        file_deepest = min([int(mode.replace('LPM', '').replace('_bits', ''))
                                            for mode in file_lpms])
                        dep_deepest = min([int(mode.replace('LPM', '').replace('_bits', ''))
                                           for mode in dep_lpms])

                        # Report if there's a significant difference in sleep modes
                        if abs(file_deepest - dep_deepest) >= 2:
                            # Create a cross-file issue
                            location = SourceLocation(file=file_path, line=lpm_by_file[file_path][0][1])

                            # Get code snippet
                            start_line = max(0, lpm_by_file[file_path][0][1] - 2)
                            end_line = min(len(file_lines), lpm_by_file[file_path][0][1] + 3)
                            code_snippet = "\n".join(file_lines[start_line:end_line])

                            issue = DeepEnergyIssue(
                                issue_type="inconsistent_sleep_modes",
                                location=location,
                                description=f"Inconsistent sleep modes between related files",
                                impact=0.55,
                                suggestion=f"Harmonize sleep modes across related files for optimal power management",
                                code_snippet=code_snippet,
                                optimization_gain=0.10,
                                related_files=[dep],
                                technical_details=f"File uses LPM{file_deepest} while related file {dep} uses LPM{dep_deepest}. Inconsistent sleep modes can lead to suboptimal power management.",
                                references=[self.references['msp430_lpm']]
                            )

                            self.result.add_issue(issue)

    def _check_clock_consistency(self, dependencies: Dict[str, List[str]]):
        """Check for consistency in clock configuration across files."""
        # Find all clock configurations
        clock_pattern = re.compile(r'(BCSCTL\d|DCOCTL|UCSCTL\d)\s*[|&^]?=\s*([^;]+)')
        clock_by_file = {}

        for file_path, content in self.code_manager.context.file_cache.items():
            if not file_path.endswith(('.c', '.h', '.cpp', '.hpp')):
                continue

            relative_path = os.path.relpath(file_path, self.project_path)
            file_lines = content.splitlines()

            for match in clock_pattern.finditer(content):
                clock_reg = match.group(1)
                config = match.group(2)
                line_number = content[:match.start()].count('\n') + 1

                if relative_path not in clock_by_file:
                    clock_by_file[relative_path] = []

                clock_by_file[relative_path].append((clock_reg, config, line_number))

        # Check for potential clock conflicts
        for file_path, clock_configs in clock_by_file.items():
            # Check if file has dependencies
            if file_path not in dependencies:
                continue

            # Extract clock frequencies from configurations
            file_frequencies = []
            for _, config, _ in clock_configs:
                if 'MHZ' in config.upper():
                    if '16' in config:
                        file_frequencies.append(16)
                    elif '12' in config:
                        file_frequencies.append(12)
                    elif '8' in config:
                        file_frequencies.append(8)
                    elif '1' in config:
                        file_frequencies.append(1)

            if not file_frequencies:
                continue

            # Check if related files use different frequencies
            for dep in dependencies[file_path]:
                if dep not in clock_by_file:
                    continue

                dep_frequencies = []
                for _, config, _ in clock_by_file[dep]:
                    if 'MHZ' in config.upper():
                        if '16' in config:
                            dep_frequencies.append(16)
                        elif '12' in config:
                            dep_frequencies.append(12)
                        elif '8' in config:
                            dep_frequencies.append(8)
                        elif '1' in config:
                            dep_frequencies.append(1)

                if dep_frequencies and set(file_frequencies) != set(dep_frequencies):
                    # Find the line number of the clock configuration
                    line_number = clock_configs[0][2]

                    # Get code snippet
                    start_line = max(0, line_number - 2)
                    end_line = min(len(file_lines), line_number + 3)
                    code_snippet = "\n".join(file_lines[start_line:end_line])

                    # Create cross-file issue
                    location = SourceLocation(file=file_path, line=line_number)
                    issue = DeepEnergyIssue(
                        issue_type="inconsistent_clock_frequencies",
                        location=location,
                        description=f"Inconsistent clock frequencies between related files",
                        impact=0.60,
                        suggestion=f"Harmonize clock frequencies or ensure proper clock management between files",
                        code_snippet=code_snippet,
                        optimization_gain=0.15,
                        related_files=[dep],
                        technical_details=f"File uses {file_frequencies} MHz while related file {dep} uses {dep_frequencies} MHz. Inconsistent clock frequencies can lead to unexpected behavior and inefficient power usage.",
                        references=[self.references['clock_management']]
                    )

                    self.result.add_issue(issue)

    def _check_peripheral_consistency(self, dependencies: Dict[str, List[str]]):
        """Check for consistency in peripheral management across files."""
        # Find peripheral enable/disable patterns
        peripheral_patterns = {
            'uart': re.compile(r'(UCA\d|UCB\d)CTL\d\s*[|&^]?=\s*([^;]+)'),
            'adc': re.compile(r'ADC\d+CTL\d\s*[|&^]?=\s*([^;]+)'),
            'timer': re.compile(r'(TA\d+CTL|TB\d+CTL)\s*[|&^]?=\s*([^;]+)'),
            'spi': re.compile(r'(UCB\d)CTL\d\s*[|&^]?=\s*([^;]+).*?(SPI)'),
            'i2c': re.compile(r'(UCB\d)CTL\d\s*[|&^]?=\s*([^;]+).*?(I2C)')
        }

        peripheral_by_file = defaultdict(lambda: defaultdict(list))

        for file_path, content in self.code_manager.context.file_cache.items():
            if not file_path.endswith(('.c', '.h', '.cpp', '.hpp')):
                continue

            relative_path = os.path.relpath(file_path, self.project_path)
            file_lines = content.splitlines()

            for ptype, pattern in peripheral_patterns.items():
                for match in pattern.finditer(content):
                    try:
                        # Handle different group patterns safely
                        if ptype in ['spi', 'i2c']:
                            if len(match.groups()) >= 3:  # Make sure we have enough groups
                                periph_name = f"{match.group(3)}_{match.group(1)}"
                                config = match.group(2)
                            else:
                                # Skip this match if it doesn't have the expected groups
                                continue
                        else:
                            periph_name = match.group(1)
                            config = match.group(2)

                        line_number = content[:match.start()].count('\n') + 1

                        # Check if peripheral is being disabled
                        is_disabled = False
                        if 'UCSWRST' in config or '&= ~' in config or 'OFF' in config:
                            is_disabled = True

                        peripheral_by_file[relative_path][ptype].append((periph_name, config, line_number, is_disabled))
                    except IndexError:
                        # Log the error but continue processing
                        logger.warning(f"Pattern match error in {relative_path} for {ptype} pattern")
                        continue

        # Check for peripherals enabled in one file but not properly managed in related files
        for file_path, peripherals in peripheral_by_file.items():
            # Check if file has dependencies
            if file_path not in dependencies:
                continue

            # For each peripheral type in this file
            for ptype, configs in peripherals.items():
                # Find enabled peripherals that aren't disabled
                enabled_peripherals = []
                for periph_name, config, line_number, is_disabled in configs:
                    if not is_disabled and 'ENABLE' in config.upper():
                        enabled_peripherals.append((periph_name, line_number))

                if not enabled_peripherals:
                    continue

                # Check if related files properly handle these peripherals
                for dep in dependencies[file_path]:
                    if dep not in peripheral_by_file or ptype not in peripheral_by_file[dep]:
                        continue

                    dep_peripherals = peripheral_by_file[dep][ptype]

                    # For each enabled peripheral in this file
                    for periph_name, line_number in enabled_peripherals:
                        # Check if the peripheral is properly disabled in dependent file
                        is_managed = False
                        for dep_name, _, _, is_disabled in dep_peripherals:
                            if dep_name == periph_name and is_disabled:
                                is_managed = True
                                break

                        if not is_managed:
                            # Get code snippet
                            start_line = max(0, line_number - 2)
                            end_line = min(len(file_lines), line_number + 3)
                            code_snippet = "\n".join(file_lines[start_line:end_line])

                            # Create cross-file issue
                            location = SourceLocation(file=file_path, line=line_number)
                            issue = DeepEnergyIssue(
                                issue_type="peripheral_not_managed_across_files",
                                location=location,
                                description=f"{ptype.upper()} peripheral enabled but not properly managed across files",
                                impact=0.50,
                                suggestion=f"Ensure {ptype.upper()} peripheral is properly disabled in related files when not in use",
                                code_snippet=code_snippet,
                                optimization_gain=0.05,
                                related_files=[dep],
                                technical_details=f"{periph_name} is enabled in {file_path} but not properly disabled in related file {dep}. Peripherals should be disabled when not in use to save power.",
                                references=[self.references['peripheral_config']]
                            )

                            self.result.add_issue(issue)


def deep_analyze_code(project_path: str, config: Dict[str, Any] = None) -> DeepAnalysisResult:
    """Perform deep energy analysis on the specified project path."""
    analyzer = DeepCodeAnalyzer(project_path, config)
    return analyzer.analyze()


def generate_optimization_summary(result: DeepAnalysisResult) -> Dict[str, Any]:
    """Generate a summary of optimization opportunities from the analysis result."""
    summary = {
        "total_issues": len(result.issues),
        "total_files_analyzed": result.analyzed_files,
        "total_energy_impact": result.total_energy_impact,
        "total_optimization_gain": result.total_optimization_gain,
        "issue_types": dict(result.issue_types),
        "file_count": len(result.file_issues),
        "high_impact_issues": len([i for i in result.issues if i.impact >= 0.7]),
        "patterns_detected": dict([(p, len(files)) for p, files in result.patterns.items()]),
        "cross_file_issues": len(result.cross_file_issues),
        "top_issues": []
    }

    # Add top 5 issues by impact
    for issue in sorted(result.issues, key=lambda x: x.impact, reverse=True)[:5]:
        summary["top_issues"].append({
            "type": issue.issue_type,
            "description": issue.description,
            "file": issue.location.file,
            "line": issue.location.line,
            "impact": issue.impact,
            "optimization_gain": issue.optimization_gain,
            "suggestion": issue.suggestion
        })

    return summary

