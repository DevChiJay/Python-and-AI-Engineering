"""
CLI Interface Module
Provides command-line interface for the File Analyzer
"""

import os
import sys
import argparse
from pathlib import Path

# Import our custom modules
from file_analyzer.file_utils import FileValidator, FileHelper
from file_analyzer.content_analyzer import ContentAnalyzer
from file_analyzer.report_generator import ReportGenerator


class FileAnalyzerCLI:
    """
    Command Line Interface for File Analyzer
    Handles user input, file validation, and output formatting
    """
    
    def __init__(self):
        self.validator = FileValidator()
        self.helper = FileHelper()
        self.content_analyzer = ContentAnalyzer()
        self.report_generator = ReportGenerator()
    
    def display_banner(self):
        """Display welcome banner"""
        print("\n" + "=" * 50)
        print("🔍 FILE ANALYZER CLI")
        print("Analyze files and get detailed summaries")
        print("=" * 50)
    
    def get_file_path(self):
        """Get file path from user input with validation"""
        while True:
            print("\n📁 Enter file path (or 'quit' to exit):")
            file_path = input(">>> ").strip()
            
            # Handle quit command
            if file_path.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                return None
            
            # Handle empty input
            if not file_path:
                print("❌ Please enter a valid file path.")
                continue
            
            # Remove quotes if present
            file_path = file_path.strip('"\'')
            
            # Convert to absolute path
            file_path = os.path.abspath(file_path)
            
            # Validate file existence
            if not self.validator.file_exists(file_path):
                print(f"❌ File not found or not accessible: {file_path}")
                print("   Please check the path and try again.")
                continue
            
            # Validate file size
            if not self.validator.is_file_size_valid(file_path):
                size = self.helper.format_file_size(self.validator.get_file_size(file_path))
                max_size = self.helper.format_file_size(self.validator.MAX_FILE_SIZE)
                print(f"❌ File too large: {size} (max: {max_size})")
                continue
            
            return file_path
    
    def get_output_format(self):
        """Get preferred output format from user"""
        print("\n📊 Choose output format:")
        print("1. Detailed Summary (default)")
        print("2. Quick Summary")
        print("3. JSON Format")
        
        choice = input("Enter choice (1-3): ").strip()
        
        format_map = {
            '1': 'detailed',
            '2': 'quick', 
            '3': 'json',
            '': 'detailed'  # default
        }
        
        return format_map.get(choice, 'detailed')
    
    def analyze_file(self, file_path):
        """Perform complete file analysis"""
        print(f"\n🔍 Analyzing: {os.path.basename(file_path)}")
        print("   Please wait...")
        
        try:
            # Get basic file information
            file_info = self.helper.get_file_info(file_path)
            
            # Analyze content based on file type
            content_analysis = self.content_analyzer.analyze_content(
                file_path, file_info['type']
            )
            
            return file_info, content_analysis
            
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
            return None, None
    
    def display_results(self, file_info, content_analysis, output_format):
        """Display analysis results in requested format"""
        
        if not file_info or not content_analysis:
            print("❌ No results to display.")
            return
        
        print("\n" + "=" * 60)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 60)
        
        # Generate and display report based on format
        if output_format == 'quick':
            summary = self.report_generator.generate_quick_summary(file_info, content_analysis)
            print(f"\n📋 Quick Summary:\n{summary}")
            
        elif output_format == 'json':
            json_report = self.report_generator.generate_json_report(file_info, content_analysis)
            print("\n📄 JSON Report:")
            print(json_report)
            
        else:  # detailed
            detailed_report = self.report_generator.generate_summary_report(file_info, content_analysis)
            print(detailed_report)
    
    def save_report_option(self, file_info, content_analysis, output_format):
        """Offer option to save report to file"""
        save_choice = input("\n💾 Save report to file? (y/n): ").strip().lower()
        
        if save_choice in ['y', 'yes']:
            # Generate filename based on original file
            original_name = Path(file_info['name']).stem
            timestamp = self.helper.get_file_info(file_info['path'])
            
            if output_format == 'json':
                report_name = f"{original_name}_analysis.json"
                report_content = self.report_generator.generate_json_report(file_info, content_analysis)
            else:
                report_name = f"{original_name}_analysis.txt"
                report_content = self.report_generator.generate_summary_report(file_info, content_analysis)
            
            try:
                with open(report_name, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                print(f"✅ Report saved as: {report_name}")
            except Exception as e:
                print(f"❌ Error saving report: {str(e)}")
    
    def run_interactive_mode(self):
        """Run the CLI in interactive mode"""
        self.display_banner()
        
        while True:
            # Get file path from user
            file_path = self.get_file_path()
            if file_path is None:  # User wants to quit
                break
            
            # Get output format preference
            output_format = self.get_output_format()
            
            # Analyze the file
            file_info, content_analysis = self.analyze_file(file_path)
            
            # Display results
            self.display_results(file_info, content_analysis, output_format)
            
            # Offer to save report
            if file_info and content_analysis:
                self.save_report_option(file_info, content_analysis, output_format)
            
            # Ask if user wants to analyze another file
            print("\n" + "-" * 50)
            continue_choice = input("Analyze another file? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                print("👋 Thank you for using File Analyzer!")
                break
    
    def run_single_file_mode(self, file_path, output_format='detailed', save_report=False):
        """Run analysis for a single file (for command-line arguments)"""
        
        # Validate file
        if not self.validator.file_exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False
        
        if not self.validator.is_file_size_valid(file_path):
            print(f"❌ File too large: {self.helper.format_file_size(self.validator.get_file_size(file_path))}")
            return False
        
        # Analyze file
        file_info, content_analysis = self.analyze_file(file_path)
        
        if not file_info:
            return False
        
        # Display results
        self.display_results(file_info, content_analysis, output_format)
        
        # Save report if requested
        if save_report:
            self.save_report_option(file_info, content_analysis, output_format)
        
        return True


def create_argument_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="File Analyzer - Analyze files and generate detailed summaries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python File-Analyzer.py                          # Interactive mode
  python File-Analyzer.py file.txt                 # Analyze single file
  python File-Analyzer.py file.py --format json   # JSON output
  python File-Analyzer.py data.csv --save          # Save report
        """
    )
    
    parser.add_argument(
        'file', 
        nargs='?', 
        help='Path to file to analyze (optional - launches interactive mode if not provided)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['detailed', 'quick', 'json'],
        default='detailed',
        help='Output format (default: detailed)'
    )
    
    parser.add_argument(
        '--save', '-s',
        action='store_true',
        help='Save report to file'
    )
    
    return parser


def main():
    """Main entry point for the File Analyzer CLI"""
    
    # Create CLI instance
    cli = FileAnalyzerCLI()
    
    # Parse command line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        if args.file:
            # Single file mode
            success = cli.run_single_file_mode(
                file_path=args.file,
                output_format=args.format,
                save_report=args.save
            )
            sys.exit(0 if success else 1)
        else:
            # Interactive mode
            cli.run_interactive_mode()
    
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


# Entry point when running this module directly
if __name__ == "__main__":
    main()
