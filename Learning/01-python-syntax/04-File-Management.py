#!/usr/bin/env python3
"""
File Management Tool - Python Basics Demonstration
This tool demonstrates Python fundamentals through a practical file management utility.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# --- Classes & OOP Demonstration ---

class FileError(Exception):
    """Custom exception for file operations - user-defined exceptions"""
    pass


class TextFile:
    """Base class for file operations - demonstrates class creation"""
    
    def __init__(self, file_path: str):
        """Constructor method - called when creating new instance"""
        self.file_path = file_path
        self.content = ""
        
    def read(self) -> str:
        """Read file content - instance method example"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:  # Context manager for file handling
                self.content = file.read()
            return self.content
        except FileNotFoundError:
            # Exception handling - catching specific exception
            raise FileError(f"File not found: {self.file_path}")
        except PermissionError:
            raise FileError(f"Permission denied: {self.file_path}")
    
    def write(self, content: str) -> None:
        """Write content to file - simple method with type hints"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            self.content = content
        except IOError as e:
            # Exception handling with error details
            raise FileError(f"Failed to write to {self.file_path}: {str(e)}")
    
    @property
    def size(self) -> int:
        """Property decorator - access method as attribute"""
        try:
            return os.path.getsize(self.file_path)
        except OSError:
            return 0


class AnalyzedFile(TextFile):
    """Inherited class - demonstrates inheritance"""
    
    def __init__(self, file_path: str):
        # Call parent constructor - super() function
        super().__init__(file_path)
        self.stats = {}
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze file content - method overriding"""
        if not self.content:
            self.read()  # Call parent method
            
        # Calculate stats
        self.stats = {
            'char_count': len(self.content),
            'word_count': len(self.content.split()),
            'line_count': len(self.content.splitlines()),
            'file_size': self.size,  # Using parent's property
            'timestamp': datetime.now().isoformat()
        }
        return self.stats
    
    def get_report(self, format_type: str = 'text') -> str:
        """Generate report - demonstrates conditionals and formatting"""
        if not self.stats:
            self.analyze()
            
        # Fancy output formatting using f-strings
        if format_type == 'json':
            return json.dumps(self.stats, indent=2)
        elif format_type == 'text':
            return f"""
File Analysis Report
-------------------
File: {self.file_path}
Size: {self.stats['file_size']} bytes
Characters: {self.stats['char_count']}
Words: {self.stats['word_count']}
Lines: {self.stats['line_count']}
Analyzed on: {self.stats['timestamp']}
"""
        else:
            # Raising exceptions - user-defined exception
            raise FileError(f"Unsupported format type: {format_type}")


# --- File Manager - Main Application Class ---

class FileManager:
    """Main application class that manages file operations"""
    
    def __init__(self):
        self.files = {}  # Dictionary to store file objects
        
    def add_file(self, file_path: str) -> AnalyzedFile:
        """Add file to manager - demonstrates dictionary usage"""
        if file_path in self.files:
            return self.files[file_path]
        
        try:
            file = AnalyzedFile(file_path)
            self.files[file_path] = file
            return file
        except Exception as e:
            # Re-raising exceptions with context
            raise FileError(f"Failed to add file {file_path}: {str(e)}") from e
    
    def analyze_all(self) -> Dict[str, Dict[str, Any]]:
        """Analyze all files - demonstrates dictionary comprehension"""
        results = {}
        for path, file in self.files.items():
            try:
                results[path] = file.analyze()
            except FileError as e:
                print(f"Warning: Could not analyze {path}: {e}", file=sys.stderr)
        return results
    
    def save_report(self, output_file: str, format_type: str = 'json') -> None:
        """Save analysis report - demonstrates file output"""
        all_stats = self.analyze_all()
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                if format_type == 'json':
                    json.dump(all_stats, f, indent=2)
                else:
                    # List comprehension to build report
                    report_lines = [
                        "File Analysis Summary Report",
                        "===========================",
                        f"Generated on: {datetime.now().isoformat()}",
                        "Files analyzed: {}".format(len(all_stats)),
                        "",
                    ]
                    
                    # Extending list with file details - demonstrates list operations
                    for path, stats in all_stats.items():
                        report_lines.extend([
                            f"File: {path}",
                            f"  Size: {stats['file_size']} bytes",
                            f"  Words: {stats['word_count']}",
                            f"  Lines: {stats['line_count']}",
                            ""
                        ])
                    
                    f.write('\n'.join(report_lines))
                    
        except IOError as e:
            raise FileError(f"Failed to save report to {output_file}: {str(e)}")


# --- Command-line interface - demonstrates standard library usage ---

def parse_arguments():
    """Parse command line arguments - demonstrates argparse library"""
    parser = argparse.ArgumentParser(description='File Management and Analysis Tool')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='Files to analyze')
    parser.add_argument('-o', '--output', type=str, default='report.txt',
                        help='Output file for the report')
    parser.add_argument('-f', '--format', choices=['text', 'json'], default='text',
                        help='Output format (text or json)')
    return parser.parse_args()


def main():
    """Main function - program entry point"""
    try:
        args = parse_arguments()
        
        # Create manager instance
        manager = FileManager()
        
        # Add all files from arguments
        for file_path in args.files:
            try:
                file = manager.add_file(file_path)
                
                # Display individual file report to console
                print(file.get_report(args.format))
                
            except FileError as e:
                print(f"Error: {e}", file=sys.stderr)
        
        # Save combined report
        manager.save_report(args.output, args.format)
        print(f"\nSummary report saved to {args.output}")
        
    except Exception as e:
        # Global exception handler - good practice
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1
    
    return 0


# --- Program Entry Point - Demonstrates module behavior ---
if __name__ == "__main__":
    # This code only runs when the script is executed directly
    sys.exit(main())  # Return exit code to OS
