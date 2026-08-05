# Use a pipeline as a high-level helper
from transformers import pipeline, infer_device, AutoTokenizer, AutoModelForCausalLM, GPT2Tokenizer, GPT2Model

checkpoint = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(checkpoint)
model = GPT2Model.from_pretrained(checkpoint)
text = "Grief has a way of "

encoded_input = tokenizer(text, return_tensors="pt")
output = model(**encoded_input)

print(output)
# device = infer_device()

# pipe = pipeline("text-generation", model="openai-community/gpt2", device=device)

# # Ensure a pad token is set (GPT-2 has no pad token by default)
# pipe.model.config.pad_token_id = pipe.model.config.eos_token_id

# out = pipe("The secret to acquiring wealth is ", max_new_tokens=50, truncation=True)

# print(out)
