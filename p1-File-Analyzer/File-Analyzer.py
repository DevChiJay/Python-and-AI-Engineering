#!/usr/bin/env python3
"""
File Analyzer - Main Entry Point
A comprehensive file analysis tool that provides detailed summaries of various file types.

This is a Python syntax learning project that demonstrates:
- Module organization and imports
- Object-oriented programming
- File I/O operations
- Error handling
- Command-line interfaces
- String manipulation and analysis

Usage:
    python File-Analyzer.py                     # Interactive mode
    python File-Analyzer.py file.txt            # Analyze single file
    python File-Analyzer.py file.py --format json  # JSON output
"""

import sys
import os

# Add the current directory to Python path so we can import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the CLI module from our file_analyzer package
from file_analyzer.cli import main

# Main execution block - this runs when the script is executed directly
if __name__ == "__main__":
    # Call the main function from the CLI module
    main()