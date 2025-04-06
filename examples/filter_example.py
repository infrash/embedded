#!/usr/bin/env python3
"""
Example script demonstrating the file filtering capabilities of the energy optimizer tool.
This script shows how to use file filtering both from the command line and programmatically.
"""

import os
import sys
import logging

# Add the parent directory to sys.path to make the package importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import from the package
from file_filter import FileFilter, create_default_filter, create_custom_filter

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("energy-optimizer.example")

def example_command_line_usage():
    """Examples of using file filtering via command line arguments."""
    print("\n===== Command Line Usage Examples =====")

    # Basic usage
    print("\n1. Basic usage - exclude backup files:")
    print("   python cli.py comment /path/to/project --exclude-patterns \".*\\.bak$\"")

    # Filter by extension
    print("\n2. Only include C and header files:")
    print("   python cli.py comment /path/to/project --include-extensions .c .h")

    # Exclude specific directories
    print("\n3. Exclude specific directories:")
    print("   python cli.py comment /path/to/project --exclude-dirs build test docs")

    # Combined filtering
    print("\n4. Combined filtering:")
    print("   python cli.py comment /path/to/project \\")
    print("     --include-extensions .c .h \\")
    print("     --exclude-dirs build test \\")
    print("     --exclude-patterns \".*\\.bak$\" \".*~$\"")

    # With other options
    print("\n5. With other command options:")
    print("   python cli.py comment /path/to/project \\")
    print("     --dry-run \\")
    print("     --format todo \\")
    print("     --min-impact 0.7 \\")
    print("     --deep-analysis \\")
    print("     --exclude-patterns \".*\\.bak$\"")


def example_programmatic_usage(project_path):
    """
    Examples of using file filtering programmatically.

    Args:
        project_path: Path to a project to scan
    """
    print("\n===== Programmatic Usage Examples =====")

    # Find all files in the project
    all_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    print(f"\nFound {len(all_files)} total files in {project_path}")

    # Example 1: Default filter
    print("\n1. Using default filter:")
    default_filter = create_default_filter()
    filtered_files = default_filter.filter_files(all_files)
    print(f"   Default filter kept {len(filtered_files)} of {len(all_files)} files")

    # Example 2: Custom filter with specific extensions
    print("\n2. Custom filter with specific extensions:")
    c_only_filter = create_custom_filter(include_only_extensions=['.c'])
    c_files = c_only_filter.filter_files(all_files)
    print(f"   C-only filter kept {len(c_files)} of {len(all_files)} files")

    # Example 3: Custom filter with specific exclude patterns
    print("\n3. Custom filter with specific exclude patterns:")
    custom_patterns = [".*\\.c$", ".*\\.h$"]  # Exclude .c and .h files (unusual but for demo)
    custom_filter = create_custom_filter(exclude_patterns=custom_patterns)
    custom_filtered = custom_filter.filter_files(all_files)
    print(f"   Custom pattern filter kept {len(custom_filtered)} of {len(all_files)} files")

    # Example 4: Direct use of FileFilter class
    print("\n4. Direct use of FileFilter class:")
    direct_filter = FileFilter(
        exclude_patterns=[".*\\.bak$", ".*~$"],
        include_only_extensions=['.c', '.h', '.cpp', '.hpp'],
        exclude_directories=['build', 'test']
    )
    direct_filtered = direct_filter.filter_files(all_files)
    print(f"   Direct filter kept {len(direct_filtered)} of {len(all_files)} files")

    # Print some examples of included and excluded files
    if filtered_files:
        print("\nExamples of included files (default filter):")
        for file in filtered_files[:3]:
            print(f"   - {os.path.relpath(file, project_path)}")
        if len(filtered_files) > 3:
            print(f"   - ... and {len(filtered_files) - 3} more")

    # Find examples of excluded files
    excluded = [f for f in all_files if f not in filtered_files]
    if excluded:
        print("\nExamples of excluded files (default filter):")
        for file in excluded[:3]:
            print(f"   - {os.path.relpath(file, project_path)}")
        if len(excluded) > 3:
            print(f"   - ... and {len(excluded) - 3} more")


def main():
    """Main function to run the examples."""
    print("File Filtering Examples for Energy Optimizer Tool")

    # Run command line usage examples
    example_command_line_usage()

    # Run programmatic usage examples if a project path is provided
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
        if os.path.isdir(project_path):
            example_programmatic_usage(project_path)
        else:
            print(f"\nError: The specified path '{project_path}' is not a directory.")
            print("Please provide a valid project directory path.")
    else:
        print("\nTo see programmatic examples with a real project, run:")
        print(f"  python {os.path.basename(__file__)} /path/to/your/project")


if __name__ == "__main__":
    main()