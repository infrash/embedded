# Examples for `cli.py`

This directory contains example scripts demonstrating the usage of the commands defined in `cli.py`.

## Usage

1. **Run the examples**  
   Execute any example script using Python:
   ```bash
   python examples/deep_analyze_example.py
   python examples/analyze_example.py
   python examples/optimize_example.py
   python examples/report_example.py
   python examples/deploy_example.py
   ```

2. **Input Parameters**  
   Each script simulates input parameters for its respective command. Modify the `args` dictionary within the script to provide custom inputs.

3. **Expected Outputs**  
   Each script prints both the input parameters and the output returned by the command function.


# Energy Optimizer Examples

This directory contains example scripts that demonstrate how to use the Energy Optimizer tool and process its output.

## Available Scripts

### 1. Direct API Usage

- **`api_usage.py`**: Demonstrates how to use the Energy Optimizer API directly to analyze a project.

```bash
python api_usage.py /path/to/your/project
```

### 2. Project Analysis

- **`analyze_project.py`**: Analyzes a specific project and prints a summary of energy issues found.

```bash
# Edit the PROJECT_PATH variable in the script first
python analyze_project.py
```

### 3. Processing Analyzer Output

- **`add_energy_comments.py`**: Adds energy optimization comments directly to your source code files.

```bash
python add_energy_comments.py analyzer_output.txt --project-root /path/to/your/project
```

- **`generate_energy_report.py`**: Generates an HTML report from analyzer output.

```bash
python generate_energy_report.py analyzer_output.txt --output energy_report.html
```

## Working with Analyzer Output

After running the energy-optimizer on your project, you can save the output to a file:

```bash
energy-optimizer analyze /path/to/your/project > analyzer_output.txt
```

Then you can use the processing scripts to:

1. **Add comments to your code**:

```bash
python add_energy_comments.py analyzer_output.txt --project-root /path/to/your/project
```

This will add comments like this to your code:

```c
/* ENERGY: peripheral_not_disabled - Ensure UART is properly disabled when not needed to save power (Impact: 0.70) */
UCA1CTL1 |= UCSWRST;
```

2. **Generate an HTML report**:

```bash
python generate_energy_report.py analyzer_output.txt
```

This will create an interactive HTML report with charts, tables and detailed information about the energy issues found.

## Additional Options

### add_energy_comments.py

```
usage: add_energy_comments.py [-h] [--project-root PROJECT_ROOT] [--no-backup] [--dry-run] issues_file

Add energy optimization comments to code files.

positional arguments:
  issues_file           Path to file containing analyzer output

options:
  -h, --help            show this help message and exit
  --project-root PROJECT_ROOT
                        Root directory of the project (for relative paths)
  --no-backup           Skip creating backup files
  --dry-run             Show what would be done without making changes
```

### generate_energy_report.py

```
usage: generate_energy_report.py [-h] [--output OUTPUT] issues_file

Generate energy optimization report.

positional arguments:
  issues_file           Path to file containing analyzer output

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output HTML report file
```