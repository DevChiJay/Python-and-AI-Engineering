"""
OpenAI API interaction module.

This module handles all interactions with the OpenAI API,
including sending requests and handling responses.
"""

import logging
import openai
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

logger = logging.getLogger(__name__)

class ChatGPTClient:
    """Client for interacting with OpenAI's ChatGPT API."""
    
    def __init__(self, api_key, model_name="gpt-3.5-turbo"):
        """
        Initialize the ChatGPT client.
        
        Args:
            api_key (str): OpenAI API key
            model_name (str): Model name to use (default: gpt-3.5-turbo)
        """
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.conversation_history = []
        logger.info(f"ChatGPT client initialized with model: {model_name}")
        
    def add_message_to_history(self, role, content):
        """
        Add a message to the conversation history.
        
        Args:
            role (str): The role of the message sender ('user' or 'assistant')
            content (str): The content of the message
        """
        self.conversation_history.append({"role": role, "content": content})
        
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")
        
    def send_message(self, message):
        """
        Send a message to the ChatGPT API and get a response.
        
        Args:
            message (str): The user's message
            
        Returns:
            str: The assistant's response
            
        Raises:
            openai.APIError: For API-related errors
            Exception: For other unexpected errors
        """
        try:
            # Add user message to history
            self.add_message_to_history("user", message)
            
            logger.debug(f"Sending message to API: {message[:50]}...")
            
            # Create the API request
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.conversation_history
            )
            
            # Extract and store the assistant's response
            assistant_message = response.choices[0].message.content
            self.add_message_to_history("assistant", assistant_message)
            
            logger.debug(f"Received response from API: {assistant_message[:50]}...")
            return assistant_message
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error when sending message: {str(e)}")
            raise
