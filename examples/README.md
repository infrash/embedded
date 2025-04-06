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


# Przykłady użycia narzędzia komentowania

Narzędzie komentowania pozwala na automatyczne dodawanie sugestii optymalizacji energetycznej do kodu źródłowego na podstawie wyników analizy. Poniżej przedstawiono kilka przykładów użycia tego narzędzia.

## Przykład 1: Podstawowe użycie z interfejsu wiersza poleceń

```bash
# Uruchomienie komendy comment dla projektu
python -m infrash_embedded.cli comment /path/to/project --format inline

# Uruchomienie w trybie dry-run (bez wprowadzania zmian)
python -m infrash_embedded.cli comment /path/to/project --dry-run

# Komentowanie tylko problemów o wysokim wpływie
python -m infrash_embedded.cli comment /path/to/project --min-impact 0.7

# Generowanie raportu markdown
python -m infrash_embedded.cli comment /path/to/project --output report.md
```

## Przykład 2: Użycie skryptu przykładowego comment_example.py

```bash
# Przejdź do katalogu examples
cd examples

# Uruchom przykład komentowania
python comment_example.py

# Uruchomienie z własnymi parametrami (wymaga edycji skryptu)
# - Otwórz comment_example.py
# - Zmień parametry w klasie Args
# - Uruchom skrypt ponownie
```

## Przykład 3: Użycie niestandardowego narzędzia custom_comment_tool.py

```bash
# Komentowanie projektu z domyślnymi ustawieniami (próg wpływu 0.7, komentarze inline)
python custom_comment_tool.py /path/to/project

# Komentowanie wszystkich problemów (próg wpływu 0.0)
python custom_comment_tool.py /path/to/project --min-impact 0.0

# Używanie formatu TODO zamiast inline
python custom_comment_tool.py /path/to/project --format todo

# Uruchomienie bez tworzenia kopii zapasowych plików
python custom_comment_tool.py /path/to/project --no-backup

# Podgląd zmian bez ich wprowadzania (tryb dry-run)
python custom_comment_tool.py /path/to/project --dry-run
```

## Przykłady rezultatów komentowania

### Format Inline:

```c
while(1) { // ENERGY: Busy-wait pattern detected - wastes energy by keeping CPU active - Replace busy-wait with low power mode and interrupts (Impact: 0.75, Gain: 0.15)
  // Kod wewnątrz pętli
}
```

### Format TODO:

```c
// TODO ENERGY: Busy-wait pattern detected - wastes energy by keeping CPU active - Replace busy-wait with low power mode and interrupts (Impact: 0.75, Gain: 0.15)
while(1) {
  // Kod wewnątrz pętli
}
```

## Zalecany przepływ pracy

1. **Analiza projektu**: Najpierw wykonaj analizę głęboką aby zidentyfikować problemy energetyczne
2. **Komentowanie w trybie dry-run**: Sprawdź, jakie zmiany zostaną wprowadzone
3. **Selektywne komentowanie**: Zacznij od problemów o wysokim wpływie (--min-impact 0.7)
4. **Przegląd i poprawki**: Przeglądnij dodane komentarze i wprowadź poprawki
5. **Powtórna analiza**: Po wprowadzeniu poprawek, wykonaj ponowną analizę, aby sprawdzić efekty

## Wskazówki

- Używaj trybu `--dry-run` przed wprowadzeniem rzeczywistych zmian
- Zawsze twórz kopie zapasowe plików (domyślnie włączone)
- Zacznij od komentowania tylko problemów o wysokim wpływie
- Format `inline` jest bardziej kompaktowy, ale może powodować długie linie
- Format `todo` jest bardziej widoczny i nie zaburza oryginalnego kodu