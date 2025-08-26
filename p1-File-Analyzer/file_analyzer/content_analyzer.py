"""
Content Analyzer Module
Analyzes file content based on file type and provides summaries
"""

import os
import json
import csv
from collections import Counter
import re
from datetime import datetime


class TextAnalyzer:
    """
    Analyzes text-based files and provides detailed statistics
    """
    
    @staticmethod
    def analyze_text_file(file_path):
        """Analyze text file content and return statistics"""
        try:
            # Try different encodings to handle various text files
            encodings = ['utf-8', 'utf-16', 'ascii', 'latin-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                return {"error": "Could not decode file with supported encodings"}
            
            # Calculate basic statistics
            lines = content.split('\n')
            words = content.split()
            characters = len(content)
            characters_no_spaces = len(content.replace(' ', '').replace('\n', '').replace('\t', ''))
            
            # Find most common words (excluding very short words)
            word_pattern = re.compile(r'\b[a-zA-Z]{3,}\b')
            meaningful_words = word_pattern.findall(content.lower())
            common_words = Counter(meaningful_words).most_common(5)
            
            return {
                'total_lines': len(lines),
                'total_words': len(words),
                'total_characters': characters,
                'characters_no_spaces': characters_no_spaces,
                'average_words_per_line': round(len(words) / max(len(lines), 1), 2),
                'common_words': common_words,
                'encoding_used': encoding
            }
            
        except Exception as e:
            return {"error": f"Error analyzing text file: {str(e)}"}


class CodeAnalyzer:
    """
    Analyzes code files and provides programming-specific insights
    """
    
    @staticmethod
    def analyze_python_file(file_path):
        """Analyze Python file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            lines = content.split('\n')
            
            # Count different elements
            imports = len([line for line in lines if line.strip().startswith(('import ', 'from '))])
            functions = len([line for line in lines if line.strip().startswith('def ')])
            classes = len([line for line in lines if line.strip().startswith('class ')])
            comments = len([line for line in lines if line.strip().startswith('#')])
            docstrings = content.count('"""') // 2 + content.count("'''") // 2
            
            # Calculate complexity (rough estimate)
            complexity_keywords = ['if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except:', 'with ']
            complexity = sum(content.count(keyword) for keyword in complexity_keywords)
            
            return {
                'type': 'Python Code',
                'imports': imports,
                'functions': functions,
                'classes': classes,
                'comments': comments,
                'docstrings': docstrings,
                'estimated_complexity': complexity,
                'total_lines': len(lines),
                'blank_lines': len([line for line in lines if not line.strip()])
            }
            
        except Exception as e:
            return {"error": f"Error analyzing Python file: {str(e)}"}


class DataAnalyzer:
    """
    Analyzes data files like CSV, JSON
    """
    
    @staticmethod
    def analyze_csv_file(file_path):
        """Analyze CSV file structure and content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Detect delimiter
                sample = file.read(1024)
                file.seek(0)
                
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.reader(file, delimiter=delimiter)
                rows = list(reader)
                
            if not rows:
                return {"error": "CSV file is empty"}
            
            headers = rows[0] if rows else []
            data_rows = rows[1:] if len(rows) > 1 else []
            
            # Analyze columns
            column_analysis = {}
            if data_rows and headers:
                for i, header in enumerate(headers):
                    column_data = [row[i] if i < len(row) else '' for row in data_rows]
                    column_analysis[header] = {
                        'non_empty_count': len([val for val in column_data if val.strip()]),
                        'unique_values': len(set(column_data)),
                        'sample_values': column_data[:3]
                    }
            
            return {
                'type': 'CSV Data',
                'total_rows': len(rows),
                'data_rows': len(data_rows),
                'columns': len(headers),
                'headers': headers,
                'delimiter': delimiter,
                'column_analysis': column_analysis
            }
            
        except Exception as e:
            return {"error": f"Error analyzing CSV file: {str(e)}"}
    
    @staticmethod
    def analyze_json_file(file_path):
        """Analyze JSON file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            def analyze_json_structure(obj, depth=0):
                """Recursively analyze JSON structure"""
                if isinstance(obj, dict):
                    return {
                        'type': 'object',
                        'keys': len(obj.keys()),
                        'key_names': list(obj.keys())[:10],  # Show first 10 keys
                        'max_depth': depth
                    }
                elif isinstance(obj, list):
                    return {
                        'type': 'array',
                        'length': len(obj),
                        'item_types': list(set(type(item).__name__ for item in obj[:10])),
                        'max_depth': depth
                    }
                else:
                    return {
                        'type': type(obj).__name__,
                        'max_depth': depth
                    }
            
            structure = analyze_json_structure(data)
            
            return {
                'type': 'JSON Data',
                'structure': structure,
                'estimated_size': len(json.dumps(data))
            }
            
        except Exception as e:
            return {"error": f"Error analyzing JSON file: {str(e)}"}


class ContentAnalyzer:
    """
    Main content analyzer that routes to appropriate sub-analyzers
    """
    
    @staticmethod
    def analyze_content(file_path, file_type):
        """Analyze file content based on its type"""
        
        # Get file extension for more specific analysis
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Route to appropriate analyzer based on file type and extension
        if file_type == 'text':
            if file_extension == '.py':
                return CodeAnalyzer.analyze_python_file(file_path)
            elif file_extension == '.csv':
                return DataAnalyzer.analyze_csv_file(file_path)
            elif file_extension == '.json':
                return DataAnalyzer.analyze_json_file(file_path)
            else:
                return TextAnalyzer.analyze_text_file(file_path)
        
        elif file_type in ['image', 'document', 'archive']:
            return {
                'type': file_type.title(),
                'message': f"Binary {file_type} file - content analysis not available",
                'suggestion': "Use specialized tools for detailed analysis of this file type"
            }
        
        else:
            return {
                'type': 'Unknown',
                'message': "File type not supported for content analysis"
            }
