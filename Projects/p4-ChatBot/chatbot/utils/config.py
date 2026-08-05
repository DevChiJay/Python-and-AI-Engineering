"""
Environment configuration utility module.

This module handles loading environment variables from the .env file
and provides access to configuration settings for the application.
"""

import os
import logging
from dotenv import load_dotenv

# Configure logger
logger = logging.getLogger(__name__)

def load_config():
    """
    Load environment variables from .env file.
    
    Returns:
        dict: Dictionary containing configuration values
        
    Raises:
        FileNotFoundError: If .env file is not found
        ValueError: If required environment variables are not set
    """
    try:            
        load_dotenv()
        
        # Get required configuration values
        api_key = os.getenv('OPENAI_API_KEY')
        model_name = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')  # Default to gpt-3.5-turbo if not specified
        
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        return {
            'api_key': api_key,
            'model_name': model_name
        }
        
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        raise
