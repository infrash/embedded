"""
Examples of how to use the file filtering options with the comment command.
"""

# Example command to exclude backup files and only process .c and .h files
# python cli.py comment /path/to/project --include-extensions .c .h --exclude-patterns ".*\.bak$"

# Example command to exclude backup files and specific directories
# python cli.py comment /path/to/project --exclude-dirs build test --exclude-patterns ".*\.bak$"

# Example command to only process files with high impact issues and exclude backup files
# python cli.py comment /path/to/project --min-impact 0.7 --exclude-patterns ".*\.bak$"

# Example command to do a dry run to see what would be processed
# python cli.py comment /path/to/project --dry-run --exclude-patterns ".*\.bak$"

# Example command to use todo-style comments and exclude backup files
# python cli.py comment /path/to/project --format todo --exclude-patterns ".*\.bak$"

# Example command to use deep analysis, exclude backup files, and generate a report
# python cli.py comment /path/to/project --deep-analysis --exclude-patterns ".*\.bak$" --report

# Example command with all options
# python cli.py comment /path/to/project \
#   --dry-run \
#   --format todo \
#   --min-impact 0.7 \
#   --deep-analysis \
#   --mcu-type msp430 \
#   --report \
#   --output report.md \
#   --include-extensions .c .h .cpp \
#   --exclude-dirs build test \
#   --exclude-patterns ".*\.bak$" ".*~$" ".*\.tmp$"

"""
Some more complex examples:
"""

# Exclude backup files, temporary files, and object files
EXCLUDE_BACKUP_AND_TEMP = [
    ".*\.bak$",       # Backup files
    ".*~$",           # Temporary files with tilde
    ".*\.tmp$",       # Temporary files with .tmp extension
    ".*\.o$",         # Object files
    ".*\.obj$"        # Windows object files
]

# Example of using the file filter directly in Python code
def example_file_filter_usage():
    from file_filter import FileFilter

    # Create a filter that only includes C and header files but excludes backups and temp files
    file_filter = FileFilter(
        exclude_patterns=EXCLUDE_BACKUP_AND_TEMP,
        include_only_extensions=['.c', '.h'],
        exclude_directories=['build', 'test', 'docs']
    )

    # Example list of files to filter
    files = [
        'src/main.c',
        'src/main.c.bak',
        'include/header.h',
        'include/header.h~',
        'build/output.o',
        'test/test_module.c',
        'src/module.c',
        'docs/api.md'
    ]

    # Filter the files
    filtered_files = file_filter.filter_files(files)

    print("Original files:", files)
    print("Filtered files:", filtered_files)
    # Should output: ['src/main.c', 'include/header.h', 'src/module.c']