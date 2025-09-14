"""
File handler module for reading and writing email lists.
"""

class FileHandler:
    def read_emails(self, file_path):
        """
        Read emails from a text file.
        
        Args:
            file_path (str): Path to the input file
            
        Returns:
            list: List of emails read from the file
            
        Raises:
            FileNotFoundError: If the input file does not exist
        """
        try:
            with open(file_path, 'r') as file:
                # Read all lines and strip whitespace
                emails = [line.strip() for line in file.readlines()]
                # Remove empty lines
                return [email for email in emails if email]
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading input file: {str(e)}")
    
    def write_emails(self, file_path, emails):
        """
        Write emails to a text file.
        
        Args:
            file_path (str): Path to the output file
            emails (list): List of emails to write
            
        Raises:
            Exception: If there's an error writing to the file
        """
        try:
            with open(file_path, 'w') as file:
                for email in emails:
                    file.write(f"{email}\n")
        except Exception as e:
            raise Exception(f"Error writing output file: {str(e)}")
