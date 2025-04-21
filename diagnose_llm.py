import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load Gemma 2B from Hugging Face Hub
model_id = "google/gemma-2b"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32)

# Move to CPU (since Replit doesn’t have GPU and minimal RAM)
device = torch.device("cpu")
model.to(device)

def get_llm_diagnosis(user_input: str) -> str:
    inputs = tokenizer(user_input, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            top_k=50,
            pad_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)