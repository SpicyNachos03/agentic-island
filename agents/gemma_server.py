"""
Gemma HTTP API Server for ASUS Ascent GX10.
Run this on the ASUS machine to serve Gemma via HTTP API.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import uvicorn

app = FastAPI(title="Gemma API Server")

# Configuration
MODEL_ID = "google/gemma-4-2b-it"
HOST = "0.0.0.0"
PORT = 8000

# Load model and tokenizer
print(f"Loading model: {MODEL_ID}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_4bit=True
)

print("Model loaded successfully!")


class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.95
    do_sample: bool = True


class GenerateResponse(BaseModel):
    generated_text: str


@app.get("/")
def read_root():
    return {"message": "Gemma API Server is running", "model": MODEL_ID}


@app.get("/health")
def health_check():
    return {"status": "healthy", "model": MODEL_ID}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    """Generate text using Gemma model."""
    
    inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            do_sample=request.do_sample,
            pad_token_id=tokenizer.eos_token_id
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the generated part (after the prompt)
    if request.prompt in generated_text:
        generated_text = generated_text[len(request.prompt):].strip()
    
    return GenerateResponse(generated_text=generated_text)


if __name__ == "__main__":
    print(f"Starting Gemma API server on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
