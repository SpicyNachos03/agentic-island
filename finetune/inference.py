import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from pathlib import Path

MODEL_ID = "google/gemma-7b-it"  # Gemma 2 instruction-tuned
FINETUNED_MODEL_PATH = Path(__file__).parent / "checkpoints" / "final_model"
MAX_NEW_TOKENS = 200


def load_model():
    """Load the fine-tuned model"""
    print("Loading base model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token
    
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_4bit=True
    )
    
    print("Loading fine-tuned adapter...")
    model = PeftModel.from_pretrained(base_model, str(FINETUNED_MODEL_PATH))
    model = model.merge_and_unload()
    
    return model, tokenizer


def generate_dialogue(model, tokenizer, speaker: str, previous_speaker: str = None) -> str:
    """Generate dialogue for a given speaker"""
    instruction = f"Generate dialogue for {speaker} in a reality dating show context"
    
    if previous_speaker:
        input_text = f"Context: Previous speaker was {previous_speaker}"
        prompt = f"<start_of_turn>user\n{instruction}\n\n{input_text}<end_of_turn>\n<start_of_turn>model\n"
    else:
        prompt = f"<start_of_turn>user\n{instruction}<end_of_turn>\n<start_of_turn>model\n"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=0.8,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the model's response
    response = generated_text.split("<start_of_turn>model\n")[-1]
    response = response.replace("<end_of_turn>", "").strip()
    
    return response


def simulate_conversation(model, tokenizer, num_turns: int = 6):
    """Simulate a multi-turn conversation"""
    speakers = ["Kendall", "Nicole", "Kassy", "Aaron", "Kaylor", "Kenny"]
    previous_speaker = None
    
    print("\n=== Simulated Love Island Conversation ===\n")
    
    for i in range(num_turns):
        speaker = speakers[i % len(speakers)]
        dialogue = generate_dialogue(model, tokenizer, speaker, previous_speaker)
        
        print(f"{speaker}: {dialogue}\n")
        previous_speaker = speaker


def main():
    """Run inference with the fine-tuned model"""
    print("Loading model...")
    model, tokenizer = load_model()
    
    print("Model loaded successfully!\n")
    
    # Test single generation
    print("=== Single Generation Test ===")
    speaker = "Kendall"
    dialogue = generate_dialogue(model, tokenizer, speaker)
    print(f"{speaker}: {dialogue}\n")
    
    # Simulate conversation
    simulate_conversation(model, tokenizer, num_turns=6)


if __name__ == "__main__":
    main()
