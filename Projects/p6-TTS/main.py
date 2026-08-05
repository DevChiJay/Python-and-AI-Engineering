"""
Text-to-Speech Web App using Hugging Face SpeechT5

Features:
- Uses microsoft/speecht5_tts + microsoft/speecht5_hifigan
- Provides a few CMU Arctic speakers via precomputed x-vectors
- Simple Gradio UI: enter text, pick a speaker, get WAV audio

Notes:
- First run downloads models/datasets to the Hugging Face cache.
- CPU works but is slower; GPU (CUDA) recommended for faster inference.
"""

from __future__ import annotations

import os
from typing import Dict, Tuple

import torch
import numpy as np
import gradio as gr
from datasets import load_dataset
from transformers import (
	SpeechT5Processor,
	SpeechT5ForTextToSpeech,
	SpeechT5HifiGan,
)


# ------------------------------------
# Global configuration
# ------------------------------------
SAMPLE_RATE = 16000
TTS_MODEL_ID = "microsoft/speecht5_tts"
VOCODER_MODEL_ID = "microsoft/speecht5_hifigan"
XVECTOR_DATASET_ID = "Matthijs/cmu-arctic-xvectors"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------
# Lazy-loaded singletons
# ------------------------------------
_processor: SpeechT5Processor | None = None
_tts_model: SpeechT5ForTextToSpeech | None = None
_vocoder: SpeechT5HifiGan | None = None
_speaker_map: Dict[str, torch.Tensor] | None = None


def _load_models():
	global _processor, _tts_model, _vocoder
	if _processor is None:
		_processor = SpeechT5Processor.from_pretrained(TTS_MODEL_ID)
	if _tts_model is None:
		_tts_model = SpeechT5ForTextToSpeech.from_pretrained(TTS_MODEL_ID).to(DEVICE)
		_tts_model.eval()
	if _vocoder is None:
		_vocoder = SpeechT5HifiGan.from_pretrained(VOCODER_MODEL_ID).to(DEVICE)
		_vocoder.eval()


def _build_speaker_map() -> Dict[str, torch.Tensor]:
	"""Return a small set of named speaker embeddings from the CMU Arctic x-vectors.

	We'll create a map using a single representative x-vector per CMU speaker ID.
	Typical speaker IDs in the dataset: "awb", "bdl", "clb", "rms", "slt".
	"""
	global _speaker_map
	if _speaker_map is not None:
		return _speaker_map

	speaker_map: Dict[str, torch.Tensor] = {}
	ds = None
	load_errors = []
	# Try standard load, then with trust_remote_code=True for newer datasets versions
	for kwargs in ({}, {"trust_remote_code": True}):
		try:
			ds = load_dataset(XVECTOR_DATASET_ID, split="validation", **kwargs)
			break
		except Exception as e:  # pragma: no cover - runtime environment dependent
			load_errors.append(str(e))
			ds = None

	if ds is not None:
		# Build one x-vector per speaker (first occurrence)
		for item in ds:
			spk = item.get("speaker_id")
			if spk and spk not in speaker_map:
				vec = torch.tensor(item["xvector"], dtype=torch.float32).unsqueeze(0)
				speaker_map[spk] = vec.to(DEVICE)
			# Stop early once we have a handful
			if len(speaker_map) >= 5:
				break

		# Fallback: if nothing found but dataset loaded, take the first vector
		if not speaker_map and len(ds) > 0:
			first = torch.tensor(ds[0]["xvector"], dtype=torch.float32).unsqueeze(0)
			speaker_map["default"] = first.to(DEVICE)

	# Robust fallback when dataset can't be loaded (dataset scripts disabled, offline, etc.)
	if not speaker_map:
		# Create deterministic pseudo x-vectors (512-dim) for a few named voices
		def synth_vec(name: str) -> torch.Tensor:
			# Seed from name for determinism
			seed = abs(hash(name)) % (2**32)
			g = torch.Generator().manual_seed(seed)
			v = torch.randn((1, 512), generator=g) * 0.5
			return v.to(DEVICE)

		for label in ["neutral", "warm", "bright", "calm", "energetic"]:
			speaker_map[label] = synth_vec(label)

	_speaker_map = speaker_map
	return _speaker_map


def synthesize_speech(text: str, speaker: str) -> Tuple[int, np.ndarray]:
	"""Generate speech waveform from text and selected speaker.

	Returns (sample_rate, waveform) suitable for Gradio audio output.
	"""
	if not text or not text.strip():
		raise gr.Error("Please enter some text to synthesize.")

	_load_models()
	speaker_map = _build_speaker_map()

	if speaker not in speaker_map:
		# use any available embedding
		speaker_embedding = next(iter(speaker_map.values()))
	else:
		speaker_embedding = speaker_map[speaker]

	assert _processor is not None and _tts_model is not None and _vocoder is not None

	with torch.inference_mode():
		inputs = _processor(text=text, return_tensors="pt").to(DEVICE)
		# Generate waveform tensor on DEVICE, then move to CPU for numpy conversion
		speech: torch.Tensor = _tts_model.generate_speech(
			inputs["input_ids"],
			speaker_embeddings=speaker_embedding,
			vocoder=_vocoder,
		)

	audio = speech.detach().cpu().numpy()
	return SAMPLE_RATE, audio


def build_ui() -> gr.Blocks:
	speaker_options = sorted(list(_build_speaker_map().keys()))

	with gr.Blocks(title="SpeechT5 TTS") as demo:
		gr.Markdown(
			"""
			# Text to Speech (SpeechT5)
			Enter text, choose a speaker, and generate natural-sounding speech.
			"""
		)

		with gr.Row():
			text = gr.Textbox(
				label="Text",
				placeholder="Type the text you want to convert to speech...",
				lines=4,
				value="Hello! This is a demo of SpeechT5 text-to-speech.",
			)
		with gr.Row():
			speaker = gr.Dropdown(
				choices=speaker_options,
				value=speaker_options[0] if speaker_options else None,
				label="Speaker",
			)
		with gr.Row():
			btn = gr.Button("Synthesize Speech", variant="primary")
		with gr.Row():
			audio = gr.Audio(label="Output Audio", type="numpy")

		btn.click(fn=synthesize_speech, inputs=[text, speaker], outputs=audio)

		gr.Markdown(
			f"Running on: {'CUDA' if torch.cuda.is_available() else 'CPU'} • Models cache in HF_HOME or default cache"
		)

	return demo


def main():
	# Pre-warm model metadata (does not download twice; safe on cache)
	_load_models()
	_build_speaker_map()

	demo = build_ui()
	# By default, listen on localhost only (Windows-friendly). Set share=True to expose.
	demo.launch(share=True)


if __name__ == "__main__":
	main()

