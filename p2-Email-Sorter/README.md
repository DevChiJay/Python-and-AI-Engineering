# Email Sorter Application

A Python application that processes email lists from text files and performs various cleaning operations.

## Features

- Remove duplicate email addresses
- Remove invalid email addresses (emails without '@' or containing special characters)
- Save the processed list to a new file

## Requirements

- Python 3.6 or higher

## Usage

### Basic Usage

```bash
python main.py input_file.txt -d -i
```

Where:
- `input_file.txt` is your file containing the list of emails (one email per line)
- `-d` flag enables removing duplicates
- `-i` flag enables removing invalid emails

### Command Line Arguments

```
usage: main.py [-h] [-o OUTPUT] [-d] [-i] input_file

Email Sorter - Process email lists

positional arguments:
  input_file            Path to the input file containing emails

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to the output file (default: input_file_processed.txt)
  -d, --duplicates      Remove duplicate emails
  -i, --invalid         Remove invalid emails
```

## Examples

### Remove Duplicates Only

```bash
python main.py emails.txt -d
```

### Remove Invalid Emails Only

```bash
python main.py emails.txt -i
```

### Remove Both Duplicates and Invalid Emails

```bash
python main.py emails.txt -d -i
```

### Specify Output File

```bash
python main.py emails.txt -d -i -o cleaned_emails.txt
```

## Email Validation Rules

An email is considered invalid if it:
- Does not contain the '@' character
- Contains special characters like '/', ',', '\', or spaces
- Does not follow the general email format (username@domain.tld)
