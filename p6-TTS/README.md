# SpeechT5 Text-to-Speech Web App

A simple web app that converts text to speech using Hugging Face's SpeechT5 TTS model and Gradio.

- TTS: `microsoft/speecht5_tts`
- Vocoder: `microsoft/speecht5_hifigan`
- Speaker embeddings: `Matthijs/cmu-arctic-xvectors`

## Features
- Enter any text and pick a speaker (e.g., awb, bdl, clb, rms, slt)
- Generates a WAV audio output at 16 kHz
- Works on CPU; CUDA GPU recommended for speed

## Setup

1) Create/activate a virtual environment (recommended)

```bash
# in Windows Bash (Git Bash) or WSL
python -m venv .venv
source .venv/Scripts/activate
```

2) Install PyTorch

- CPU only (works everywhere):
```bash
pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

- Or install CUDA build (if you have an NVIDIA GPU). Refer to https://pytorch.org/get-started/locally/ for the correct index URL for your CUDA version, for example:
```bash
# Example for CUDA 12.1 (check the official site for latest):
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

3) Install remaining dependencies

```bash
pip install -r requirements.txt
```

## Run the app

```bash
python main.py
```

- The first run will download the models and the x-vectors dataset to your Hugging Face cache.
- The app will open a local Gradio interface; open the printed URL in your browser.

## Troubleshooting
- If downloads are slow or blocked, set `HF_HUB_ENABLE_HF_TRANSFER=1` to speed up via `hf_transfer` (optional).
- If CUDA is available but not used, ensure your PyTorch was installed with the correct CUDA build and your GPU drivers are up to date.
- Memory: On CPU expect several seconds per generation. On GPU it's faster.

### Dataset script error
If you see an error like:

```
RuntimeError: Dataset scripts are no longer supported, but found cmu-arctic-xvectors.py
```

Recent versions of `datasets` deprecate certain script-based datasets. This app now:
1) Tries loading with `trust_remote_code=True` automatically;
2) If loading still fails, it falls back to deterministic synthetic speaker embeddings (labeled `neutral`, `warm`, `bright`, `calm`, `energetic`).

The fallback keeps the app usable. If you want real x-vectors, consider pinning `datasets` to a version that supports the dataset or using your own speaker embeddings.

## Notes
- This demo loads a small set of speakers from `Matthijs/cmu-arctic-xvectors`. You can replace speaker embeddings with your own x-vector.
- For production, consider wrapping this in FastAPI and serving a `/synthesize` endpoint that returns WAV bytes.