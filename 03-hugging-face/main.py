# Use a pipeline as a high-level helper
from transformers import pipeline, infer_device

device = infer_device()

pipe = pipeline("text-generation", model="openai-community/gpt2", device=device)

# Ensure a pad token is set (GPT-2 has no pad token by default)
pipe.model.config.pad_token_id = pipe.model.config.eos_token_id

out = pipe("The secret to acquiring wealth is ", max_new_tokens=50, truncation=True)

print(out)
