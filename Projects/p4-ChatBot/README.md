# ChatGPT CLI Chatbot

A simple command-line interface chatbot that integrates with OpenAI's ChatGPT API.

## Features

- Interactive command-line interface
- Integration with OpenAI's ChatGPT API
- Conversation history management
- Error handling and logging
- Colorful and user-friendly output

## Prerequisites

- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository or download the source code.
2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Configure your OpenAI API key by creating a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-3.5-turbo
```

## Usage

1. Run the chatbot:

```bash
python main.py
```

2. Start chatting with the bot by typing messages and pressing Enter.

## Commands

- `/quit` or `/exit` - Exit the application
- `/clear` - Clear the conversation history
- `/help` - Show help message

## Project Structure

```
p4-ChatBot/
│
├── .env                      # Environment variables (API keys)
├── main.py                   # Main application entry point
├── requirements.txt          # Project dependencies
│
├── chatbot/                  # Chatbot package
│   ├── __init__.py
│   ├── ai_client.py          # OpenAI API client
│   │
│   └── utils/                # Utility modules
│       ├── __init__.py
│       ├── cli_utils.py      # CLI interface utilities
│       ├── config.py         # Configuration management
│       └── logging_utils.py  # Logging setup
│
└── logs/                     # Log files directory
```

## Error Handling

The application includes comprehensive error handling for:
- API errors
- Network issues
- User input errors
- Configuration problems

## Logging

Logs are stored in the `logs/` directory with the naming format `chatbot_YYYYMMDD.log`.

## License

This project is licensed under the MIT License.
