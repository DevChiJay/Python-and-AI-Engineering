# File Analyzer 🔍

A comprehensive Python CLI tool for analyzing various file types and generating detailed summaries. This project is designed as a Python syntax learning exercise that demonstrates key programming concepts.

## Features

- **Multi-format Support**: Analyzes text files, Python code, CSV data, JSON files, and more
- **Detailed Analysis**: Provides statistics like word count, line count, complexity metrics
- **Multiple Output Formats**: Choose between detailed summary, quick summary, or JSON output
- **Interactive CLI**: User-friendly command-line interface with guided prompts
- **File Safety**: Built-in validation for file size and accessibility
- **Report Generation**: Option to save analysis reports to files

## Project Structure

```
01-python-syntax/
├── File-Analyzer.py          # Main entry point
├── requirements.txt          # Dependencies (uses standard library only)
├── README.md                # This documentation
└── file_analyzer/           # Main package directory
    ├── __init__.py          # Package initialization
    ├── cli.py               # Command-line interface
    ├── file_utils.py        # File validation and helper functions
    ├── content_analyzer.py  # Content analysis for different file types
    └── report_generator.py  # Report formatting and generation
```

## Usage

### Interactive Mode (Recommended for beginners)
```bash
python File-Analyzer.py
```
This launches an interactive session where you can:
1. Enter file paths when prompted
2. Choose output format (detailed/quick/JSON)
3. Save reports to files
4. Analyze multiple files in one session

### Command Line Mode
```bash
# Analyze a single file with detailed output
python File-Analyzer.py myfile.txt

# Generate JSON output
python File-Analyzer.py data.csv --format json

# Quick summary format
python File-Analyzer.py script.py --format quick

# Save report to file
python File-Analyzer.py document.txt --save
```

### Command Line Options
- `--format` or `-f`: Choose output format (`detailed`, `quick`, `json`)
- `--save` or `-s`: Automatically save report to file
- `--help` or `-h`: Show help message

## Supported File Types

### Text Files (.txt, .md, etc.)
- Line and word count
- Character statistics
- Most common words
- Average words per line

### Python Code (.py)
- Import statements count
- Function and class definitions
- Comment and docstring analysis
- Complexity estimation
- Code quality metrics

### CSV Data (.csv)
- Row and column count
- Header analysis
- Data type detection
- Column statistics

### JSON Data (.json)
- Structure analysis
- Object/array detection
- Key enumeration
- Size estimation

### Other Files
- Basic file information (size, type, timestamps)
- MIME type detection
- File categorization

## Learning Concepts Demonstrated

This project showcases several important Python concepts:

### 1. **Module Organization**
```python
# Demonstrates proper package structure
from file_analyzer.cli import main
from file_analyzer.file_utils import FileValidator
```

### 2. **Object-Oriented Programming**
```python
class FileValidator:
    """Class with static methods for file validation"""
    
    @staticmethod
    def file_exists(file_path):
        return os.path.isfile(file_path)
```

### 3. **Error Handling**
```python
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
except Exception as e:
    return {"error": f"Error reading file: {str(e)}"}
```

### 4. **File I/O Operations**
```python
# Different encoding handling
encodings = ['utf-8', 'utf-16', 'ascii', 'latin-1']
for encoding in encodings:
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        break
    except UnicodeDecodeError:
        continue
```

### 5. **Command-Line Interfaces**
```python
# Using argparse for CLI functionality
parser = argparse.ArgumentParser(description="File Analyzer")
parser.add_argument('file', nargs='?', help='File to analyze')
```

### 6. **Data Analysis with Built-in Modules**
```python
# Using collections.Counter for word frequency
from collections import Counter
common_words = Counter(words).most_common(5)
```

## Example Output

### Detailed Summary
```
============================================================
FILE ANALYSIS REPORT
============================================================
Generated on: 2025-08-26 10:30:45

📁 FILE INFORMATION
------------------------------
Name: example.py
Size: 2.5 KB (2,560 bytes)
Type: Text
Extension: .py
MIME Type: text/x-python

📊 CONTENT ANALYSIS
------------------------------
Language: Python
Total Lines: 85
Functions: 4
Classes: 2
Comments: 12
Docstrings: 3
Estimated Complexity: 15
Comment Ratio: 14.1%
============================================================
```

### Quick Summary
```
example.py (2.5 KB) - Python file with 4 functions, 2 classes
```

## Installation

No external dependencies required! This project uses only Python standard library modules.

1. Clone or download the files
2. Ensure you have Python 3.6+ installed
3. Run the analyzer:
   ```bash
   python File-Analyzer.py
   ```

## Educational Value

This project helps you learn:
- **File handling**: Reading different file types and encodings
- **Data structures**: Using dictionaries, lists, and sets effectively
- **Error handling**: Graceful error management and user feedback
- **Code organization**: Splitting code into logical modules and classes
- **CLI development**: Creating user-friendly command-line tools
- **Regular expressions**: Pattern matching for text analysis
- **Data analysis**: Statistical analysis of file content

## Extension Ideas

Want to enhance this project? Try adding:
- Support for more file types (XML, YAML, etc.)
- Image metadata extraction using Pillow
- PDF text extraction
- Binary file analysis
- Performance benchmarking
- Web interface using Flask
- Database integration for storing analysis history

## Contributing

This is a learning project! Feel free to:
- Add new file type analyzers
- Improve existing analysis algorithms
- Enhance the CLI interface
- Add new output formats
- Create unit tests

---

**Happy Learning! 🐍**
