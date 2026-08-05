#!/usr/bin/env python3
"""
ChatGPT CLI Chatbot

A simple command-line interface chatbot that integrates with OpenAI's ChatGPT API.
This application demonstrates Python foundations including:
- API integration
- Environment variable management
- Error handling
- Logging
- User interface design

Author: DevChiJay
Date: September 2025
"""

import sys
import logging
import traceback
from chatbot import ChatGPTClient
from chatbot.utils import (
    load_config,
    setup_logging,
    clear_screen,
    print_welcome_message,
    print_user_message,
    print_assistant_message,
    print_system_message,
    print_error_message,
    get_user_input
)

# Set up logging
logger = setup_logging()

def handle_command(command, chat_client):
    """
    Handle special commands entered by the user.
    
    Args:
        command (str): The command entered by the user
        chat_client (ChatGPTClient): The ChatGPT client instance
        
    Returns:
        bool: True if the application should continue, False if it should exit
    """
    command = command.lower().strip()
    
    if command in ['/quit', '/exit']:
        print_system_message("Thank you for using ChatGPT CLI. Goodbye!")
        return False
    
    elif command == '/clear':
        chat_client.clear_history()
        clear_screen()
        print_welcome_message()
        print_system_message("Conversation history cleared.")
        
    elif command == '/help':
        print_welcome_message()
        
    else:
        print_error_message(f"Unknown command: {command}")
    
    return True

def main():
    """
    Main function to run the chatbot application.
    """
    try:
        # Load configuration
        logger.info("Starting ChatGPT CLI application")
        config = load_config()
        
        # Initialize ChatGPT client
        chat_client = ChatGPTClient(
            api_key=config['api_key'],
            model_name=config['model_name']
        )
        
        # Display welcome message
        clear_screen()
        print_welcome_message()
        print_system_message("ChatGPT CLI is ready. Type a message to begin.")
        
        # Main chat loop
        while True:
            # Get user input
            user_input = get_user_input()
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            # Check if the input is a command
            if user_input.startswith('/'):
                if not handle_command(user_input, chat_client):
                    break
                continue
            
            # Process regular message
            print_user_message(user_input)
            
            try:
                # Send message to ChatGPT and get response
                response = chat_client.send_message(user_input)
                print_assistant_message(response)
                
            except Exception as e:
                logger.error(f"Error getting response from ChatGPT: {str(e)}")
                print_error_message(f"Failed to get response: {str(e)}")
        
    except KeyboardInterrupt:
        print("\n")
        logger.info("Application terminated by keyboard interrupt")
        print_system_message("Application terminated. Goodbye!")
        
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")
        print_error_message(f"An unexpected error occurred: {str(e)}")
        print("Please check the log file for details.")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
