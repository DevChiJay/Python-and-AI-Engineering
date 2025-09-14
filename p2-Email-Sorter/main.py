#!/usr/bin/env python3
"""
Email Sorter Application
This application reads a text file containing emails and performs sorting operations.
"""

import argparse
from email_sorter.email_processor import EmailProcessor
from email_sorter.file_handler import FileHandler

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Email Sorter - Process email lists")
    parser.add_argument("input_file", help="Path to the input file containing emails")
    parser.add_argument("-o", "--output", default=None, 
                        help="Path to the output file (default: input_file_processed.txt)")
    parser.add_argument("-d", "--duplicates", action="store_true", 
                        help="Remove duplicate emails")
    parser.add_argument("-i", "--invalid", action="store_true", 
                        help="Remove invalid emails")
    
    args = parser.parse_args()
    
    # Set default output file if not provided
    if not args.output:
        output_file = args.input_file.rsplit('.', 1)[0] + "_processed.txt"
    else:
        output_file = args.output
    
    try:
        # Read emails from input file
        file_handler = FileHandler()
        emails = file_handler.read_emails(args.input_file)
        
        print(f"Read {len(emails)} emails from {args.input_file}")
        
        # Process emails based on selected options
        email_processor = EmailProcessor()
        
        if args.duplicates:
            emails = email_processor.remove_duplicates(emails)
            print(f"After removing duplicates: {len(emails)} emails remaining")
            
        if args.invalid:
            emails = email_processor.remove_invalid(emails)
            print(f"After removing invalid emails: {len(emails)} emails remaining")
            
        # If no operation selected, show usage
        if not (args.duplicates or args.invalid):
            print("No operation selected. Please use -d or -i options.")
            print("Use --help for more information.")
            return
            
        # Write processed emails to output file
        file_handler.write_emails(output_file, emails)
        print(f"Processed emails written to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
