# voice-bot-api

FastAPI backend for text-to-speech (multiple engines) and speech-to-text with modular architecture.

## Features
* Modular layout: `routers/`, `services/`, `utils/`
* Environment + secrets loading via `python-dotenv` (`app/config.py`)
* Text-to-Speech engines:
  * Hugging Face Inference Provider (Kokoro / fal-ai) – `/tts/generate`
  * Local SpeechT5 (no provider API required) – `/tts/local`
  * gTTS (Google Translate TTS) – `/tts/gtts`
* Speech-to-Text (ASR) via OpenAI Whisper API – `/asr/transcribe`
* Health check – `/health`
* CORS configuration with `ALLOWED_ORIGINS`

## Endpoints Summary
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/` | Root metadata |
| POST | `/tts/generate` | Remote provider Kokoro TTS (needs HF token) |
| POST | `/tts/local` | Local SpeechT5 TTS (downloads models once) |
| POST | `/tts/gtts` | gTTS MP3 synthesis |
| POST | `/asr/transcribe` | Whisper ASR transcription (needs OpenAI key) |

## Environment Variables
See `.env.example` for all. Important ones:

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | For ASR | OpenAI Whisper transcription |
| `HUGGINGFACEHUB_API_TOKEN` / `HF_TOKEN` | For `/tts/generate` | Hugging Face provider auth |
| `SPEECHT5_XVECTOR_PATH` | Optional | Custom speaker embedding (.npy / .pt) for SpeechT5 |
| `ALLOWED_ORIGINS` | Optional | CORS origins (comma-separated or `*`) |
| `ENVIRONMENT` | Optional | Environment label (default: development) |

## Requirements
Install from `requirements.txt`:
```
pip install -r requirements.txt
```

## Running Locally
1. Copy `.env.example` to `.env` and fill values.
2. Create & activate a virtual environment (recommended).
3. Install dependencies.
4. Start the server.

### Quickstart
```bash
pip install -r requirements.txt
python main.py
```
Server runs at: http://localhost:8000

### Uvicorn (explicit)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Example Requests

### Kokoro (provider) TTS
```bash
curl -X POST http://localhost:8000/tts/generate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from Kokoro"}'
```

### Local SpeechT5
```bash
curl -X POST http://localhost:8000/tts/local \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from local SpeechT5","return_base64":true}'
```

### gTTS
```bash
curl -X POST http://localhost:8000/tts/gtts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from gTTS","lang":"en","slow":false}'
```

### Whisper ASR
```bash
curl -X POST http://localhost:8000/asr/transcribe \
  -H "accept: application/json" \
  -F "file=@path/to/audio.wav"
```

## Project Structure (trimmed)
```
app/
  config.py
  routers/
    health.py
    tts.py
    asr.py
  services/
    tts_service.py
    gtts_service.py
    whisper_asr.py
  utils/
    audio_utils.py
data/
  inputs/
  outputs/
requirements.txt
.env.example
README.md
```

## Notes
* First run of SpeechT5 downloads models; allow time.
* Provide your own `SPEECHT5_XVECTOR_PATH` for consistent voice.
* gTTS calls external service (network required).
* For production, consider: rate limiting, request auth, file size limits, persistent storage (S3), and background jobs for long tasks.

## License
MIT (adjust as needed).
