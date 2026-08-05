import csv
import re

# Input and output file paths
input_file = 'data.csv'
output_file = 'emails.txt'

# Regex pattern to detect emails - more strict validation
email_pattern = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')

emails = set()  # Use a set to avoid duplicates

# Read CSV file
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for cell in row:
            found_emails = email_pattern.findall(cell)
            emails.update(email.lower() for email in found_emails)

# Write each email to a new line in the text file
with open(output_file, 'w', encoding='utf-8') as txtfile:
    for email in sorted(emails):
        txtfile.write(email + '\n')

print(f"✅ Extracted {len(emails)} emails to {output_file}")
