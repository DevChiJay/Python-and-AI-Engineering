"""
File Utilities Module
Contains helper functions for file operations and validations
"""

import os
import mimetypes
from pathlib import Path


class FileValidator:
    """
    Validates file properties and ensures file safety
    """
    
    # Define maximum file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Supported file types for analysis
    SUPPORTED_TYPES = {
        'text': ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.xml', '.csv'],
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        'document': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
        'archive': ['.zip', '.rar', '.tar', '.gz', '.7z']
    }
    
    @staticmethod
    def file_exists(file_path):
        """Check if file exists and is accessible"""
        return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
    
    @staticmethod
    def get_file_size(file_path):
        """Get file size in bytes"""
        return os.path.getsize(file_path)
    
    @staticmethod
    def is_file_size_valid(file_path):
        """Check if file size is within acceptable limits"""
        return FileValidator.get_file_size(file_path) <= FileValidator.MAX_FILE_SIZE
    
    @staticmethod
    def get_file_type(file_path):
        """Determine file type category based on extension"""
        file_extension = Path(file_path).suffix.lower()
        
        for category, extensions in FileValidator.SUPPORTED_TYPES.items():
            if file_extension in extensions:
                return category
        return 'unknown'
    
    @staticmethod
    def get_mime_type(file_path):
        """Get MIME type of the file"""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'unknown'


class FileHelper:
    """
    Helper functions for file operations
    """
    
    @staticmethod
    def format_file_size(size_bytes):
        """Convert bytes to human-readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    @staticmethod
    def get_file_info(file_path):
        """Get basic file information"""
        file_stat = os.stat(file_path)
        
        return {
            'name': os.path.basename(file_path),
            'path': os.path.abspath(file_path),
            'size': file_stat.st_size,
            'size_formatted': FileHelper.format_file_size(file_stat.st_size),
            'extension': Path(file_path).suffix.lower(),
            'type': FileValidator.get_file_type(file_path),
            'mime_type': FileValidator.get_mime_type(file_path),
            'modified_time': file_stat.st_mtime,
            'created_time': file_stat.st_ctime
        }
