#!/usr/bin/env python3
# examples/deep_analyze_example.py
"""
Example script demonstrating the deep analysis capability of the energy optimizer tool.
"""

import os
import sys

# Add the parent directory to sys.path to make the package importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now import from the package
from infrash_embedded.cli import deep_analyze_command
from infrash_embedded.deep_analyzer import deep_analyze_code

def main():
    """Run a sample deep analysis on a project directory."""
    # Use a sample project directory - replace with your actual project path
    project_path = os.path.join(os.path.dirname(__file__), '../../../zlecenia/maski/Programator_2025')

    # Create a mock args object to pass to the command
    class Args:
        def __init__(self):
            self.project_path = project_path
            self.report = True
            self.output = None
            self.no_cross_file = False
            self.no_patterns = False
            self.no_fix_examples = False
            self.mcu_type = 'msp430'

    args = Args()

    # Call the deep analyze command
    print(f"Running deep analysis on {project_path}")
    deep_analyze_command(args)

    # Alternative: call the deep_analyze_code function directly
    print("\nAlternative approach - calling deep_analyze_code directly:")
    config = {
        'cross_file_analysis': True,
        'pattern_detection': True,
        'mcu_specific': True,
        'find_fix_examples': True
    }
    result = deep_analyze_code(project_path, config)
    print(f"Analysis complete. Found {len(result.issues)} issues.")

if __name__ == "__main__":
    main()