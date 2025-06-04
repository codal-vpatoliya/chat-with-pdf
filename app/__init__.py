from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen1.5-1.8B-Chat"

# This will download and cache the model locally (e.g., ~/.cache/huggingface)
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
