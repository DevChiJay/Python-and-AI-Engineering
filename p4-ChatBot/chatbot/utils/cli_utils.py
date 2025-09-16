"""
CLI utility module.

This module provides functions for enhancing the command-line interface,
including colored output and user input handling.
"""

import os
import sys
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

logger = logging.getLogger(__name__)

def clear_screen():
    """Clear the terminal screen based on operating system."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/Mac
        os.system('clear')

def print_welcome_message():
    """Print a welcome message to the user."""
    welcome_text = """
    ╔═══════════════════════════════════════╗
    ║           CHATGPT CLI CHATBOT         ║
    ╚═══════════════════════════════════════╝
    
    Type your messages and press Enter to chat.
    Commands:
      /quit or /exit - Exit the application
      /clear - Clear the conversation history
      /help - Show this help message
    """
    print(Fore.CYAN + welcome_text)

def print_user_message(message):
    """
    Print a user message with formatting.
    
    Args:
        message (str): The message to print
    """
    print(f"{Fore.GREEN}You: {Style.RESET_ALL}{message}")

def print_assistant_message(message):
    """
    Print an assistant message with formatting.
    
    Args:
        message (str): The message to print
    """
    print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}{message}")

def print_system_message(message):
    """
    Print a system message with formatting.
    
    Args:
        message (str): The message to print
    """
    print(f"{Fore.YELLOW}System: {Style.RESET_ALL}{message}")

def print_error_message(message):
    """
    Print an error message with formatting.
    
    Args:
        message (str): The error message to print
    """
    print(f"{Fore.RED}Error: {Style.RESET_ALL}{message}")

def get_user_input(prompt="You: "):
    """
    Get user input with a prompt.
    
    Args:
        prompt (str): The prompt to display
        
    Returns:
        str: The user's input
    """
    try:
        return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error getting user input: {str(e)}")
        print_error_message("An error occurred while reading input.")
        return ""
