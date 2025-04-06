"""
File filtering configuration for the energy optimization tool.
This module provides functions to filter files that should be excluded from analysis.
"""

import os
import re
from typing import List, Set, Pattern

# Default exclusion patterns
DEFAULT_EXCLUDE_PATTERNS = [
    r'.*\.bak$',          # Backup files (.bak)
    r'.*\.BAK$',          # Backup files (.BAK)
    r'.*~$',              # Temporary files (file~)
    r'.*\.tmp$',          # Temporary files (.tmp)
    r'.*\.temp$',         # Temporary files (.temp)
    r'.*\.orig$',         # Original files (.orig)
    r'.*\.old$',          # Old files (.old)
    r'.*\.swp$',          # Vim swap files (.swp)
    r'.*\.swo$',          # Vim swap files (.swo)
    r'build/.*',          # Build directory
    r'dist/.*',           # Distribution directory
    r'\.git/.*',          # Git directory
    r'\.vscode/.*',       # VS Code directory
    r'\.idea/.*',         # IntelliJ directory
    r'__pycache__/.*',    # Python cache directory
    r'.*\.pyc$',          # Python compiled files
    r'.*\.pyo$',          # Python optimized files
    r'.*\.DS_Store$',     # macOS specific files
    r'.*\.vs$',           # Visual Studio directory
    r'.*\.o$',            # Object files
    r'.*\.a$',            # Static library files
    r'.*\.so$',           # Shared library files
    r'.*\.dll$',          # Windows DLL files
    r'.*\.exe$',          # Windows executable files
    r'.*\.obj$',          # Windows object files
    r'.*\.lib$',          # Windows library files
    r'.*\.out$',          # Unix executable files
]

class FileFilter:
    """File filter for the energy optimization tool."""

    def __init__(self, exclude_patterns: List[str] = None,
                 include_only_extensions: List[str] = None,
                 exclude_directories: List[str] = None):
        """
        Initialize the file filter.

        Args:
            exclude_patterns: Regex patterns for files to exclude
            include_only_extensions: File extensions to include (e.g., ['.c', '.h'])
            exclude_directories: Directory names to exclude
        """
        # Use default patterns if none provided
        self.exclude_patterns = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS

        # Compile regex patterns for better performance
        self.exclude_regex: List[Pattern] = [re.compile(pattern) for pattern in self.exclude_patterns]

        # Extensions to include (normalize to include the dot)
        self.include_only_extensions: Set[str] = set()
        if include_only_extensions:
            for ext in include_only_extensions:
                if not ext.startswith('.'):
                    ext = '.' + ext
                self.include_only_extensions.add(ext.lower())

        # Directories to exclude
        self.exclude_directories = set(exclude_directories or [])

    def should_exclude(self, file_path: str) -> bool:
        """
        Check if a file should be excluded from analysis.

        Args:
            file_path: Path to the file

        Returns:
            True if the file should be excluded, False otherwise
        """
        # Get normalized path and filename
        norm_path = os.path.normpath(file_path)
        file_name = os.path.basename(norm_path)

        # Check if in excluded directory
        for directory in self.exclude_directories:
            dir_path = os.path.normpath(directory)
            if dir_path in norm_path.split(os.sep):
                return True

        # Check extension if include_only_extensions is specified
        if self.include_only_extensions:
            _, ext = os.path.splitext(file_name)
            if ext.lower() not in self.include_only_extensions:
                return True

        # Check against exclude patterns
        for pattern in self.exclude_regex:
            if pattern.match(norm_path) or pattern.match(file_name):
                return True

        return False

    def filter_files(self, file_list: List[str]) -> List[str]:
        """
        Filter a list of files according to the exclusion rules.

        Args:
            file_list: List of file paths

        Returns:
            Filtered list of file paths
        """
        return [f for f in file_list if not self.should_exclude(f)]


# Example usage
def create_default_filter(include_only_extensions=None, exclude_directories=None):
    """
    Create a default file filter.

    Args:
        include_only_extensions: File extensions to include (e.g., ['.c', '.h'])
        exclude_directories: Directory names to exclude

    Returns:
        FileFilter object
    """
    return FileFilter(
        exclude_patterns=DEFAULT_EXCLUDE_PATTERNS,
        include_only_extensions=include_only_extensions or ['.c', '.h', '.cpp', '.hpp'],
        exclude_directories=exclude_directories
    )