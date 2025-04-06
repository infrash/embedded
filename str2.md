embedded/
│
├── src/
│   └── infrash_embedded/         # Główny katalog pakietu
│       ├── __init__.py           # Inicjalizacja pakietu
│       ├── _version.py           # Informacje o wersji
│       ├── cli.py                # Interfejs wiersza poleceń
│       ├── analyzer.py           # Podstawowy analizator kodu
│       ├── deep_analyzer.py      # Zaawansowany analizator energetyczny
│       └── optimization.py       # Moduł optymalizacji kodu
│
├── examples/                     # Przykłady użycia narzędzi
│   ├── deep_analyze_example.py   # Przykład głębokiej analizy
│   ├── comment_example.py        # Przykład komentowania kodu
│   ├── custom_comment_tool.py    # Niestandardowe narzędzie komentujące
│   └── sample_project/           # Przykładowy projekt do analizy
│       ├── main.c
│       └── [inne pliki projektu]
│
├── tools/                        # Narzędzia pomocnicze
│   ├── comment_adder_script.py   # Skrypt do dodawania komentarzy
│   └── report_generator.py       # Generator raportów
│
├── docs/                         # Dokumentacja
│   ├── usage_examples.md         # Przykłady użycia
│   ├── fix_examples.md           # Przykłady poprawek
│   └── optimization_guide.md     # Przewodnik optymalizacji
│
├── tests/                        # Testy
│   ├── test_analyzer.py
│   ├── test_deep_analyzer.py
│   └── test_comment_tool.py
│
├── setup.py                      # Plik konfiguracyjny do instalacji pakietu
├── README.md                     # Główny plik README projektu
└── LICENSE                       # Informacje o licencji