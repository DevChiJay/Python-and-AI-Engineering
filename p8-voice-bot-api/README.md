# voice-bot-api

FastAPI starter for a voice bot backend with modular structure (routers, services, utils) and .env loader.

## Features
- Modular app layout: `routers/`, `services/`, `utils/`
- `.env` loading via `python-dotenv` in `app/config.py`
- Health check at `/health`

## Requirements
See `requirements.txt`.

## Running locally
1. (Optional) create a `.env` file at the project root with keys like:
   ```env
   ENVIRONMENT=development
   OPENAI_API_KEY=sk-...
   HUGGINGFACEHUB_API_TOKEN=hf_...
   ```
2. Install dependencies
3. Start the server

### Quickstart
- Using uvicorn:

```bash
# From project root
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- Or run as a module:
```bash
python -m app.main
```

Open http://localhost:8000/health to verify.

## Project structure
```
voice-bot-api/
  app/
    __init__.py
    config.py
    main.py
    routers/
      health.py
    services/
    utils/
  requirements.txt
  README.md
  .env.example
```
