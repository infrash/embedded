import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from infrash_embedded.analyzer import (
    SourceLocation,
    EnergyIssue,
    AnalysisContext,
    CodeParser,
    LoopAnalyzer,
    SleepModeAnalyzer,
    CodeAnalysisManager
)


class TestEnergyIssue(unittest.TestCase):
    def test_energy_issue_creation(self):
        """Test creation of an EnergyIssue object."""
        location = SourceLocation(file="test.c", line=10)
        issue = EnergyIssue(
            issue_type="test_issue",
            location=location,
            description="Test description",
            impact=0.5,
            suggestion="Test suggestion",
            code_snippet="int a = 5;"
        )

        self.assertEqual(issue.issue_type, "test_issue")
        self.assertEqual(issue.location.file, "test.c")
        self.assertEqual(issue.location.line, 10)
        self.assertEqual(issue.description, "Test description")
        self.assertEqual(issue.impact, 0.5)
        self.assertEqual(issue.suggestion, "Test suggestion")
        self.assertEqual(issue.code_snippet, "int a = 5;")

    def test_energy_issue_string_representation(self):
        """Test the string representation of an EnergyIssue."""
        location = SourceLocation(file="test.c", line=10)
        issue = EnergyIssue(
            issue_type="test_issue",
            location=location,
            description="Test description",
            impact=0.5,
            suggestion="Test suggestion"
        )

        expected_str = "test.c:10 - Test description (Impact: 0.50)"
        self.assertEqual(str(issue), expected_str)


class TestAnalysisContext(unittest.TestCase):
    def test_context_initialization(self):
        """Test initialization of an AnalysisContext object."""
        with tempfile.TemporaryDirectory() as temp_dir:
            context = AnalysisContext(project_path=temp_dir)

            self.assertEqual(context.project_path, os.path.abspath(temp_dir))
            self.assertEqual(context.config, {})
            self.assertEqual(context.issues, [])
            self.assertEqual(context.file_cache, {})
            self.assertEqual(context.ast_cache, {})


class TestCodeParser(unittest.TestCase):
    def test_detect_language(self):
        """Test language detection based on file extension."""
        with tempfile.TemporaryDirectory() as temp_dir:
            context = AnalysisContext(project_path=temp_dir)
            parser = CodeParser(context)

            self.assertEqual(parser.detect_language("test.c"), "c")
            self.assertEqual(parser.detect_language("test.h"), "c")
            self.assertEqual(parser.detect_language("test.cpp"), "cpp")
            self.assertEqual(parser.detect_language("test.hpp"), "cpp")
            self.assertEqual(parser.detect_language("test.py"), "python")
            self.assertEqual(parser.detect_language("test.asm"), "assembly")
            self.assertEqual(parser.detect_language("test.unknown"), "c")  # Default for embedded


class TestLoopAnalyzer(unittest.TestCase):
    @patch('infrash_embedded.analyzer.random.random')
    def test_is_inefficient_loop(self, mock_random):
        """Test detection of inefficient loops."""
        with tempfile.TemporaryDirectory() as temp_dir:
            context = AnalysisContext(project_path=temp_dir)
            analyzer = LoopAnalyzer(context)

            # Function calls in loop condition
            self.assertTrue(analyzer._is_inefficient_loop("i < getSize()"))

            # Complex calculations in loop condition
            self.assertTrue(analyzer._is_inefficient_loop("i < x * y + z"))

            # Simple increment is efficient
            self.assertFalse(analyzer._is_inefficient_loop("i += 1"))

            # Simple comparison is efficient
            self.assertFalse(analyzer._is_inefficient_loop("i < 100"))


class TestSleepModeAnalyzer(unittest.TestCase):
    def test_power_modes_hierarchy(self):
        """Test the efficiency ordering of power modes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            context = AnalysisContext(project_path=temp_dir)
            analyzer = SleepModeAnalyzer(context)

            # Check that LPM4 is more efficient than LPM0
            self.assertGreater(analyzer.POWER_MODES['LPM4'], analyzer.POWER_MODES['LPM0'])

            # Check that power modes are ordered correctly
            self.assertLess(analyzer.POWER_MODES['LPM0'], analyzer.POWER_MODES['LPM1'])
            self.assertLess(analyzer.POWER_MODES['LPM1'], analyzer.POWER_MODES['LPM2'])
            self.assertLess(analyzer.POWER_MODES['LPM2'], analyzer.POWER_MODES['LPM3'])
            self.assertLess(analyzer.POWER_MODES['LPM3'], analyzer.POWER_MODES['LPM4'])

    def test_suggest_better_power_mode(self):
        """Test suggestions for better power modes based on context."""
        with tempfile.TemporaryDirectory() as temp_dir:
            context = AnalysisContext(project_path=temp_dir)
            analyzer = SleepModeAnalyzer(context)

            # Long delay should suggest a more efficient mode
            better_mode = analyzer._suggest_better_power_mode('LPM0', "We need a long delay here")
            self.assertIsNotNone(better_mode)
            self.assertGreater(analyzer.POWER_MODES[better_mode], analyzer.POWER_MODES['LPM0'])

            # Context with RTC should suggest LPM3 for LPM0
            better_mode = analyzer._suggest_better_power_mode('LPM0', "Using RTC for wake-up")
            self.assertEqual(better_mode, 'LPM3')

            # Already using the most efficient mode should not suggest anything
            better_mode = analyzer._suggest_better_power_mode('LPM4', "Using RTC for wake-up")
            self.assertIsNone(better_mode)


class TestCodeAnalysisManager(unittest.TestCase):
    @patch('infrash_embedded.analyzer.CodeParser')
    @patch('infrash_embedded.analyzer.AnalyzerFactory')
    def test_analyze_project(self, mock_factory, mock_parser):
        """Test the overall project analysis flow."""
        # Create a mock analyzer that returns some issues
        mock_analyzer = MagicMock()
        mock_analyzer.analyze.return_value = [
            EnergyIssue(
                issue_type="test_issue",
                location=SourceLocation(file="test.c", line=10),
                description="Test description",
                impact=0.5,
                suggestion="Test suggestion"
            )
        ]

        # Set up factory to return our mock analyzer
        mock_factory.create_analyzers.return_value = [mock_analyzer]

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file
            test_file = os.path.join(temp_dir, "test.c")
            with open(test_file, 'w') as f:
                f.write('int main() { return 0; }')

            # Create the manager
            manager = CodeAnalysisManager(temp_dir)

            # Patch the _scan_files method to use our test file
            with patch.object(manager, '_scan_files') as mock_scan:
                def scan_side_effect():
                    manager.context.file_cache[test_file] = 'int main() { return 0; }'

                mock_scan.side_effect = scan_side_effect

                # Run the analysis
                issues = manager.analyze_project()

                # Verify results
                self.assertEqual(len(issues), 1)
                self.assertEqual(issues[0].issue_type, "test_issue")
                self.assertEqual(issues[0].impact, 0.5)


if __name__ == '__main__':
    unittest.main()