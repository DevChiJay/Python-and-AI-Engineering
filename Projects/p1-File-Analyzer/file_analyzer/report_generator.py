"""
Report Generator Module
Generates formatted reports and summaries for analyzed files
"""

from datetime import datetime
import json


class ReportGenerator:
    """
    Generates various types of reports for file analysis
    """
    
    @staticmethod
    def generate_summary_report(file_info, content_analysis):
        """Generate a comprehensive summary report"""
        
        # Header section with basic file information
        report = []
        report.append("=" * 60)
        report.append("FILE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # File Information Section
        report.append("📁 FILE INFORMATION")
        report.append("-" * 30)
        report.append(f"Name: {file_info['name']}")
        report.append(f"Path: {file_info['path']}")
        report.append(f"Size: {file_info['size_formatted']} ({file_info['size']:,} bytes)")
        report.append(f"Type: {file_info['type'].title()}")
        report.append(f"Extension: {file_info['extension']}")
        report.append(f"MIME Type: {file_info['mime_type']}")
        
        # Format timestamps
        modified_time = datetime.fromtimestamp(file_info['modified_time'])
        created_time = datetime.fromtimestamp(file_info['created_time'])
        report.append(f"Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Created: {created_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Content Analysis Section
        if content_analysis and 'error' not in content_analysis:
            report.append("📊 CONTENT ANALYSIS")
            report.append("-" * 30)
            
            # Handle different types of content analysis
            if content_analysis.get('type') == 'Python Code':
                ReportGenerator._add_python_analysis(report, content_analysis)
            elif content_analysis.get('type') == 'CSV Data':
                ReportGenerator._add_csv_analysis(report, content_analysis)
            elif content_analysis.get('type') == 'JSON Data':
                ReportGenerator._add_json_analysis(report, content_analysis)
            elif 'total_words' in content_analysis:  # Text file
                ReportGenerator._add_text_analysis(report, content_analysis)
            else:
                ReportGenerator._add_generic_analysis(report, content_analysis)
                
        elif content_analysis and 'error' in content_analysis:
            report.append("❌ CONTENT ANALYSIS ERROR")
            report.append("-" * 30)
            report.append(f"Error: {content_analysis['error']}")
            
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    @staticmethod
    def _add_python_analysis(report, analysis):
        """Add Python-specific analysis to report"""
        report.append(f"Language: Python")
        report.append(f"Total Lines: {analysis['total_lines']}")
        report.append(f"Blank Lines: {analysis['blank_lines']}")
        report.append(f"Code Lines: {analysis['total_lines'] - analysis['blank_lines']}")
        report.append(f"Imports: {analysis['imports']}")
        report.append(f"Functions: {analysis['functions']}")
        report.append(f"Classes: {analysis['classes']}")
        report.append(f"Comments: {analysis['comments']}")
        report.append(f"Docstrings: {analysis['docstrings']}")
        report.append(f"Estimated Complexity: {analysis['estimated_complexity']}")
        
        # Calculate code quality metrics
        if analysis['total_lines'] > 0:
            comment_ratio = (analysis['comments'] / analysis['total_lines']) * 100
            report.append(f"Comment Ratio: {comment_ratio:.1f}%")
    
    @staticmethod
    def _add_csv_analysis(report, analysis):
        """Add CSV-specific analysis to report"""
        report.append(f"Format: CSV (Delimiter: '{analysis['delimiter']}')")
        report.append(f"Total Rows: {analysis['total_rows']}")
        report.append(f"Data Rows: {analysis['data_rows']}")
        report.append(f"Columns: {analysis['columns']}")
        
        if analysis['headers']:
            report.append(f"Headers: {', '.join(analysis['headers'][:5])}")
            if len(analysis['headers']) > 5:
                report.append(f"  ... and {len(analysis['headers']) - 5} more")
        
        # Show column analysis summary
        if analysis['column_analysis']:
            report.append("")
            report.append("Column Details:")
            for col_name, col_info in list(analysis['column_analysis'].items())[:3]:
                report.append(f"  {col_name}: {col_info['non_empty_count']} filled, "
                            f"{col_info['unique_values']} unique values")
    
    @staticmethod
    def _add_json_analysis(report, analysis):
        """Add JSON-specific analysis to report"""
        report.append(f"Format: JSON")
        structure = analysis['structure']
        report.append(f"Root Type: {structure['type']}")
        
        if structure['type'] == 'object':
            report.append(f"Keys: {structure['keys']}")
            if structure['key_names']:
                report.append(f"Key Names: {', '.join(structure['key_names'][:5])}")
        elif structure['type'] == 'array':
            report.append(f"Array Length: {structure['length']}")
            report.append(f"Item Types: {', '.join(structure['item_types'])}")
        
        report.append(f"Estimated Size: {analysis['estimated_size']:,} characters")
    
    @staticmethod
    def _add_text_analysis(report, analysis):
        """Add text file analysis to report"""
        report.append(f"Encoding: {analysis.get('encoding_used', 'Unknown')}")
        report.append(f"Lines: {analysis['total_lines']:,}")
        report.append(f"Words: {analysis['total_words']:,}")
        report.append(f"Characters: {analysis['total_characters']:,}")
        report.append(f"Characters (no spaces): {analysis['characters_no_spaces']:,}")
        report.append(f"Average words per line: {analysis['average_words_per_line']}")
        
        if analysis['common_words']:
            report.append("")
            report.append("Most Common Words:")
            for word, count in analysis['common_words']:
                report.append(f"  {word}: {count} times")
    
    @staticmethod
    def _add_generic_analysis(report, analysis):
        """Add generic analysis for unsupported file types"""
        if analysis.get('message'):
            report.append(analysis['message'])
        if analysis.get('suggestion'):
            report.append(f"Suggestion: {analysis['suggestion']}")
    
    @staticmethod
    def generate_json_report(file_info, content_analysis):
        """Generate a JSON format report for programmatic use"""
        return json.dumps({
            'timestamp': datetime.now().isoformat(),
            'file_info': file_info,
            'content_analysis': content_analysis
        }, indent=2)
    
    @staticmethod
    def generate_quick_summary(file_info, content_analysis):
        """Generate a brief one-line summary"""
        file_type = file_info['type']
        size = file_info['size_formatted']
        name = file_info['name']
        
        if content_analysis and 'error' not in content_analysis:
            if content_analysis.get('type') == 'Python Code':
                return f"{name} ({size}) - Python file with {content_analysis['functions']} functions, {content_analysis['classes']} classes"
            elif content_analysis.get('total_words'):
                return f"{name} ({size}) - Text file with {content_analysis['total_words']} words, {content_analysis['total_lines']} lines"
            elif content_analysis.get('type') == 'CSV Data':
                return f"{name} ({size}) - CSV with {content_analysis['data_rows']} rows, {content_analysis['columns']} columns"
        
        return f"{name} ({size}) - {file_type.title()} file"
