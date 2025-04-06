import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from infrash_embedded.cli import (
    analyze_command,
    optimize_command,
    report_command,
    deploy_command,
    main
)


class TestCliCommands(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = self.temp_dir.name

    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    @patch('infrash_embedded.cli.CodeAnalyzer')
    @patch('sys.stdout', new_callable=StringIO)
    def test_analyze_command(self, mock_stdout, mock_analyzer):
        """Test the analyze command."""
        # Set up mock analyzer
        analyzer_instance = mock_analyzer.return_value
        analyzer_instance.analyze.return_value = [
            MagicMock(
                issue_type="test_issue",
                file="test.c",
                line=10,
                description="Test description",
                impact=0.5,
                suggestion="Test suggestion",
                __str__=lambda self: "test.c:10 - Test description (Impact: 0.50)"
            )
        ]

        # Create a mock arguments object
        args = MagicMock(
            project_path=self.project_path,
            report=False,
            output=None
        )

        # Run the command
        analyze_command(args)

        # Check that the analyzer was called with the correct arguments
        mock_analyzer.assert_called_once_with(self.project_path)
        analyzer_instance.analyze.assert_called_once()

        # Check that output contains the expected information
        output = mock_stdout.getvalue()
        self.assertIn("Analyzing project", output)
        self.assertIn("Found 1 potential energy issues", output)
        self.assertIn("test.c:10 - Test description", output)

    @patch('infrash_embedded.cli.CodeAnalyzer')
    @patch('infrash_embedded.cli.CodeOptimizer')
    @patch('sys.stdout', new_callable=StringIO)
    def test_optimize_command(self, mock_stdout, mock_optimizer, mock_analyzer):
        """Test the optimize command."""
        # Set up mock analyzer
        analyzer_instance = mock_analyzer.return_value
        analyzer_instance.analyze.return_value = [MagicMock() for _ in range(3)]

        # Set up mock optimizer
        optimizer_instance = mock_optimizer.return_value
        optimizer_instance.optimize.return_value = {
            'total_issues': 3,
            'fixed_issues': 2,
            'estimated_energy_reduction': 0.15,
            'modified_files': ['test1.c', 'test2.c']
        }

        # Create a mock arguments object
        args = MagicMock(
            project_path=self.project_path,
            report=False,
            output=None
        )

        # Run the command
        optimize_command(args)

        # Check that the analyzer and optimizer were called with the correct arguments
        mock_analyzer.assert_called_once_with(self.project_path)
        analyzer_instance.analyze.assert_called_once()
        mock_optimizer.assert_called_once_with(self.project_path, analyzer_instance.analyze.return_value)
        optimizer_instance.optimize.assert_called_once()

        # Check that output contains the expected information
        output = mock_stdout.getvalue()
        self.assertIn("Optimizing project", output)
        self.assertIn("Fixed 2 out of 3 issues", output)
        self.assertIn("Estimated energy reduction: 15.0%", output)
        self.assertIn("Modified 2 files", output)

    @patch('infrash_embedded.cli.CodeAnalyzer')
    @patch('infrash_embedded.cli.ReportGenerator')
    @patch('sys.stdout', new_callable=StringIO)
    def test_report_command(self, mock_stdout, mock_report_generator, mock_analyzer):
        """Test the report command."""
        # Set up mock analyzer
        analyzer_instance = mock_analyzer.return_value
        analyzer_instance.analyze.return_value = [MagicMock() for _ in range(2)]

        # Set up mock report generator
        report_generator_instance = mock_report_generator.return_value
        report_generator_instance.generate_report.return_value = "Test report content"

        # Create a mock arguments object
        args = MagicMock(
            project_path=self.project_path,
            format="text",
            output=None
        )

        # Run the command
        report_command(args)

        # Check that the analyzer and report generator were called with the correct arguments
        mock_analyzer.assert_called_once_with(self.project_path)
        analyzer_instance.analyze.assert_called_once()
        mock_report_generator.assert_called_once_with(self.project_path, analyzer_instance.analyze.return_value)
        report_generator_instance.generate_report.assert_called_once_with(format_type="text")

        # Check that output contains the expected information
        output = mock_stdout.getvalue()
        self.assertIn("Generating report", output)
        self.assertIn("Test report content", output)

    @patch('infrash_embedded.cli.Deployer')
    @patch('sys.stdout', new_callable=StringIO)
    def test_deploy_command(self, mock_stdout, mock_deployer):
        """Test the deploy command."""
        # Set up mock deployer
        deployer_instance = mock_deployer.return_value
        deployer_instance.deploy.return_value = True

        # Create a mock arguments object
        args = MagicMock(
            project_path=self.project_path,
            server="git@github.com:user/repo.git"
        )

        # Run the command
        deploy_command(args)

        # Check that the deployer was called with the correct arguments
        mock_deployer.assert_called_once_with(self.project_path, "git@github.com:user/repo.git")
        deployer_instance.deploy.assert_called_once()

        # Check that output contains the expected information
        output = mock_stdout.getvalue()
        self.assertIn("Deploying project", output)
        self.assertIn("Deployment successful", output)

    @patch('infrash_embedded.cli.analyze_command')
    @patch('infrash_embedded.cli.argparse.ArgumentParser.parse_args')
    def test_main_analyze(self, mock_parse_args, mock_analyze_command):
        """Test the main function with the analyze command."""
        # Set up mock arguments
        mock_args = MagicMock(
            command="analyze",
            project_path=self.project_path,
            verbose=0,
            func=mock_analyze_command
        )
        mock_parse_args.return_value = mock_args

        # Run the main function
        with patch('sys.argv', ['energy-optimizer', 'analyze', self.project_path]):
            main()

        # Check that the analyze command was called
        mock_analyze_command.assert_called_once_with(mock_args)


if __name__ == '__main__':
    unittest.main()