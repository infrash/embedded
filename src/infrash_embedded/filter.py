#!/usr/bin/env python3
"""
File filtering module for the Energy Optimizer tool.

This module provides functionality to filter files during analysis and comment operations,
allowing users to exclude backup files, temporary files, and other files that should not
be modified.
"""

import os
import re
import logging
from typing import List, Set, Pattern, Optional, Sequence

# Set up logging
logger = logging.getLogger("energy-optimizer.file-filter")

# Default exclusion patterns
DEFAULT_EXCLUDE_PATTERNS = [
    # Backup files
    r'.*\.bak$',          # Standard backup extension
    r'.*\.BAK$',          # Uppercase backup extension
    r'.*~$',              # Vim/Emacs-style backup files
    r'.*\.old$',          # Old version files
    r'.*\.orig$',         # Original files

    # Temporary files
    r'.*\.tmp$',          # Temporary files
    r'.*\.temp$',         # Temporary files
    r'.*\.swp$',          # Vim swap files
    r'.*\.swo$',          # Vim swap files

    # Build artifacts
    r'.*\.o$',            # Object files
    r'.*\.obj$',          # Windows object files
    r'.*\.a$',            # Static libraries
    r'.*\.so$',           # Shared libraries
    r'.*\.dll$',          # Windows DLLs
    r'.*\.lib$',          # Windows libraries
    r'.*\.exe$',          # Windows executables
    r'.*\.out$',          # Unix executable
    r'.*\.pyc$',          # Python compiled files
    r'.*\.pyo$',          # Python optimized files

    # VCS directories
    r'\.git/.*',          # Git directory
    r'\.svn/.*',          # Subversion directory
    r'\.hg/.*',           # Mercurial directory
    r'CVS/.*',            # CVS directory

    # IDE/editor directories
    r'\.vscode/.*',       # VS Code directory
    r'\.idea/.*',         # IntelliJ directory
    r'__pycache__/.*',    # Python cache directory
    r'\.vs/.*',           # Visual Studio directory

    # System files
    r'.*\.DS_Store$',     # macOS specific files
    r'Thumbs\.db$',       # Windows thumbnail cache
]

# Common directory paths to exclude
DEFAULT_EXCLUDE_DIRS = [
    'build',
    'dist',
    'out',
    'output',
    'bin',
    'obj',
    'node_modules',
    'venv',
    'env',
    '.env',
    '.venv',
]

# Default set of extensions to include for embedded systems
DEFAULT_INCLUDE_EXTENSIONS = [
    '.c', '.h',           # C
    '.cpp', '.hpp',       # C++
    '.s', '.asm',         # Assembly
    '.inc',               # Include files
]


class FileFilter:
    """File filter for the Energy Optimizer tool."""

    def __init__(self,
                 exclude_patterns: Optional[List[str]] = None,
                 include_only_extensions: Optional[List[str]] = None,
                 exclude_directories: Optional[List[str]] = None):
        """
        Initialize the file filter.

        Args:
            exclude_patterns: Regex patterns for files to exclude
            include_only_extensions: File extensions to include (e.g., ['.c', '.h'])
            exclude_directories: Directory names to exclude
        """
        # Use default patterns if none provided, or extend the provided ones
        if exclude_patterns is None:
            self.exclude_patterns = DEFAULT_EXCLUDE_PATTERNS.copy()
        else:
            self.exclude_patterns = exclude_patterns.copy()

        # Compile regex patterns for better performance
        self.exclude_regex: List[Pattern] = []
        for pattern in self.exclude_patterns:
            try:
                self.exclude_regex.append(re.compile(pattern))
            except re.error as e:
                logger.warning(f"Invalid regex pattern '{pattern}': {e}. Skipping.")

        # Extensions to include (normalize to include the dot)
        self.include_only_extensions: Set[str] = set()
        if include_only_extensions:
            for ext in include_only_extensions:
                if not ext.startswith('.'):
                    ext = '.' + ext
                self.include_only_extensions.add(ext.lower())

        # Directories to exclude
        self.exclude_directories = set(exclude_directories or DEFAULT_EXCLUDE_DIRS)

    def should_exclude(self, file_path: str) -> bool:
        """
        Check if a file should be excluded from analysis.

        Args:
            file_path: Path to the file

        Returns:
            True if the file should be excluded, False otherwise
        """
        # Get normalized path and filename
        try:
            norm_path = os.path.normpath(file_path)
            file_name = os.path.basename(norm_path)

            # Skip non-existent files
            if not os.path.exists(norm_path):
                logger.debug(f"File does not exist: {norm_path}")
                return True

            # Skip directories
            if os.path.isdir(norm_path):
                logger.debug(f"Skipping directory: {norm_path}")
                return True

            # Check if in excluded directory
            path_parts = norm_path.split(os.sep)
            for directory in self.exclude_directories:
                if directory in path_parts:
                    logger.debug(f"File {norm_path} in excluded directory {directory}")
                    return True

            # Check extension if include_only_extensions is specified
            if self.include_only_extensions:
                _, ext = os.path.splitext(file_name)
                if ext.lower() not in self.include_only_extensions:
                    logger.debug(f"File {norm_path} has excluded extension {ext}")
                    return True

            # Check against exclude patterns
            for pattern in self.exclude_regex:
                if pattern.match(norm_path) or pattern.match(file_name):
                    logger.debug(f"File {norm_path} matches exclude pattern {pattern.pattern}")
                    return True

            return False
        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")
            return True  # Exclude on error to be safe

    def filter_files(self, file_list: Sequence[str]) -> List[str]:
        """
        Filter a list of files according to the exclusion rules.

        Args:
            file_list: List of file paths

        Returns:
            Filtered list of file paths
        """
        result = [f for f in file_list if not self.should_exclude(f)]
        logger.info(f"Filtered {len(file_list) - len(result)} files out of {len(file_list)}")
        return result


def create_default_filter() -> FileFilter:
    """
    Create a default file filter that excludes backup files and includes common source files.

    Returns:
        FileFilter object with default settings
    """
    return FileFilter(
        exclude_patterns=DEFAULT_EXCLUDE_PATTERNS,
        include_only_extensions=DEFAULT_INCLUDE_EXTENSIONS,
        exclude_directories=DEFAULT_EXCLUDE_DIRS
    )


def create_custom_filter(
        exclude_patterns: Optional[List[str]] = None,
        include_only_extensions: Optional[List[str]] = None,
        exclude_directories: Optional[List[str]] = None
) -> FileFilter:
    """
    Create a custom file filter with the specified settings.

    Args:
        exclude_patterns: Regex patterns for files to exclude (added to defaults)
        include_only_extensions: File extensions to include (e.g., ['.c', '.h'])
        exclude_directories: Directory names to exclude (added to defaults)

    Returns:
        FileFilter object with custom settings
    """
    patterns = DEFAULT_EXCLUDE_PATTERNS.copy()
    if exclude_patterns:
        patterns.extend(exclude_patterns)

    dirs = DEFAULT_EXCLUDE_DIRS.copy()
    if exclude_directories:
        dirs.extend(exclude_directories)

    return FileFilter(
        exclude_patterns=patterns,
        include_only_extensions=include_only_extensions or DEFAULT_INCLUDE_EXTENSIONS,
        exclude_directories=dirs
    )


# Helper function to add file filter arguments to a command parser
def add_file_filter_args(parser):
    """
    Add file filtering arguments to a command line parser.

    Args:
        parser: argparse.ArgumentParser object to add arguments to
    """
    group = parser.add_argument_group('File filtering options')
    group.add_argument('--include-extensions', nargs='+',
                       metavar='EXT',
                       default=DEFAULT_INCLUDE_EXTENSIONS,
                       help='Only include files with these extensions (e.g., .c .h)')
    group.add_argument('--exclude-dirs', nargs='+',
                       metavar='DIR',
                       default=DEFAULT_EXCLUDE_DIRS,
                       help='Exclude directories (e.g., build test)')
    group.add_argument('--exclude-patterns', nargs='+',
                       metavar='PATTERN',
                       help='Additional regex patterns for files to exclude (e.g., ".*_test\\.c$")')
    group.add_argument('--no-default-excludes', action='store_true',
                       help='Do not use default exclusion patterns')
    return parser


if __name__ == "__main__":
    # Example usage
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 2:
        print("Usage: file_filter.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    file_filter = create_default_filter()

    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))

    filtered_files = file_filter.filter_files(all_files)

    print(f"Total files: {len(all_files)}")
    print(f"Filtered files: {len(filtered_files)}")

    # Print sample of filtered files
    for file in filtered_files[:10]:
        print(f"  {file}")

    if len(filtered_files) > 10:
        print(f"  ... and {len(filtered_files) - 10} more")