# Python & AI Engineering

A personal learning repository tracing the path from Python fundamentals to building production-ready AI-powered applications.

```
Learning/     ← structured learning by topic
Projects/     ← applied projects built along the way
```

---

## Learning Path

| Stage | Folder              | Topic          | What I Explored                                                       |
| ----- | ------------------- | -------------- | --------------------------------------------------------------------- |
| 1     | `01-python-syntax`  | Python Syntax  | CLI tools — todo list, number analyzer, contact manager, file manager |
| 2     | `01b-gui`           | GUI            | Desktop GUI app with Tkinter                                          |
| 3     | `02-fastapi-basics` | FastAPI Basics | REST API fundamentals                                                 |
| 4     | `03-hugging-face`   | Hugging Face   | Inference with pre-trained models                                     |
| 5     | `04-langchain`      | LangChain      | Chains, prompts, and RAG patterns                                     |
| 6     | `LangGraph`         | LangGraph      | Stateful AI agents with graph-based orchestration                     |
| 7     | `CrewAI`            | CrewAI         | Multi-agent crews for automated tasks                                 |
| 8     | `n8n`               | n8n Automation | Visual workflow automation — lead generation, Telegram bots, webhooks |

---

## Projects

> Quick links — click to jump to each project section.

- [🆕 Tweet Writer (CrewAI)](#-tweet-writer-crewai) ← latest
- [File Analyzer](#-file-analyzer)
- [Email Sorter](#-email-sorter)
- [Weather Bot](#-weather-bot)
- [ChatBot](#-chatbot)
- [News Summarizer](#-news-summarizer)
- [Text-to-Speech](#-text-to-speech)
- [Ask My Docs (RAG)](#-ask-my-docs-rag)
- [Voice Bot API](#-voice-bot-api)
- [AI Twitter Bot](#-ai-twitter-bot)

---

> [!NOTE]
> **Tweet Writer CrewAI** is the most recently built project — a fully autonomous multi-agent pipeline that researches a topic and posts a crafted tweet, end to end.

### 🆕 Tweet Writer (CrewAI)

Two-agent CrewAI crew: a **Tech Researcher** gathers topic context, then a **Tweet Writer** crafts and auto-posts a tweet via the Twitter API.

**Run:**

```bash
cd Projects/Tweet-Writer-CrewAI
pip install -r requirements.txt
# Set OPENAI_API_KEY + Twitter credentials in .env
python main.py "your topic here"
```

---

### 📁 File Analyzer

Multi-format file analysis CLI. Generates statistics and complexity metrics for `.txt`, `.py`, `.csv`, and `.json` files.

**Run:**

```bash
cd Projects/p1-File-Analyzer
pip install -r requirements.txt
python File-Analyzer.py <path-to-file>
```

---

### 📧 Email Sorter

Processes email lists — removes duplicates and invalid addresses with configurable CLI flags.

**Run:**

```bash
cd Projects/p2-Email-Sorter
pip install -r requirements.txt
python main.py --input mails.txt
```

---

### 🌤 Weather Bot

Fetches live weather data via a public API and exports results to JSON or CSV. Includes a mock-data mode for offline use.

**Run:**

```bash
cd Projects/p3-Weather-Bot
pip install -r requirements.txt
cp config_example.py config.py   # add your API key
python main.py
```

---

### 💬 ChatBot

Interactive CLI chatbot powered by OpenAI's ChatGPT API. Maintains conversation history and supports slash commands.

**Run:**

```bash
cd Projects/p4-ChatBot
pip install -r requirements.txt
# Set OPENAI_API_KEY in .env
python main.py
```

---

### 📰 News Summarizer

FastAPI service that fetches top headlines, summarizes them with OpenAI, and schedules daily digests.

**Run:**

```bash
cd Projects/p5-News-Summarizer
pip install -r requirements.txt
# Set OPENAI_API_KEY in .env
uvicorn main:app --reload
```

---

### 🔊 Text-to-Speech

Gradio web app that converts text to speech using Microsoft's SpeechT5 model from Hugging Face — runs fully locally.

**Run:**

```bash
cd Projects/p6-TTS
pip install -r requirements.txt
python main.py
```

---

### 🗂 Ask My Docs (RAG)

FastAPI + LangChain RAG API. Upload documents, then query them using OpenAI embeddings stored in a local Chroma vector database.

**Run:**

```bash
cd Projects/p7-Ask-My-Docs
pip install -r requirements.txt
# Set OPENAI_API_KEY in .env
uvicorn main:app --reload
```

---

### 🎙 Voice Bot API

Modular FastAPI backend supporting text-to-speech (Kokoro / SpeechT5 / gTTS) and speech-to-text (Whisper).

**Run:**

```bash
cd Projects/p8-voice-bot-api
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 🐦 AI Twitter Bot

CrewAI-powered bot that researches topics and auto-writes + posts tweets via the Twitter API on a schedule.

**Run:**

```bash
cd Projects/p9-AI-twitter-bot
pip install -r requirements.txt
# Set OPENAI_API_KEY and Twitter credentials in .env
python app/main.py
```

---

## Prerequisites

- Python 3.10+
- `pip` or a virtual environment manager (`venv`, `conda`)
- OpenAI API key (for ChatBot, News Summarizer, Ask My Docs, Voice Bot, Twitter Bot)
- Twitter developer credentials (for AI Twitter Bot)

> Each project has its own `requirements.txt`. It is recommended to use a separate virtual environment per project.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
