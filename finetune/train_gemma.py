import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
from pathlib import Path
import json

# Configuration
FAST_MODE = True  # Set to True for hackathon (faster training), False for better quality

if FAST_MODE:
    # Fast mode for hackathon (~30-60 minutes total)
    MODEL_ID = "google/gemma-4-2b-it"  # Gemma 4 2B instruction-tuned
    BATCH_SIZE = 4
    GRADIENT_ACCUMULATION_STEPS = 4
    NUM_EPOCHS = 1  # Single epoch for speed
    LEARNING_RATE = 5e-4  # Higher learning rate for single epoch
    MAX_SEQ_LENGTH = 512
    USE_4BIT = True  # Quantization for speed
    LORA_RANK = 4  # Smaller rank for faster training
else:
    # Full training for production (~6-12 hours)
    MODEL_ID = "google/gemma-4-9b-it"  # Gemma 4 9B instruction-tuned for Ascent GX10
    BATCH_SIZE = 8  # Increased for 128GB memory
    GRADIENT_ACCUMULATION_STEPS = 2  # Reduced since batch size increased
    NUM_EPOCHS = 3
    LEARNING_RATE = 2e-4
    MAX_SEQ_LENGTH = 1024  # Increased for better context
    USE_4BIT = False  # Set to True if memory issues, False for better quality on GX10
    LORA_RANK = 8

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "checkpoints"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data(file_path: Path) -> Dataset:
    """Load training data from file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f if line.strip()]
    
    return Dataset.from_dict({"text": texts})


def tokenize_function(examples, tokenizer):
    """Tokenize the dataset"""
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=MAX_SEQ_LENGTH,
        padding="max_length",
        return_tensors="pt"
    )


def main():
    print("Loading model and tokenizer...")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with optional 4-bit quantization
    if USE_4BIT:
        print("Using 4-bit quantization for memory efficiency")
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_4bit=True
        )
    else:
        print("Using full precision (no quantization)")
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    
    print("Configuring LoRA...")
    # Configure LoRA for parameter-efficient fine-tuning
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=LORA_RANK,  # rank (4 for fast mode, 8 for full)
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        inference_mode=False
    )
    
    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    print("Loading and tokenizing data...")
    # Load datasets
    train_dataset = load_data(DATA_DIR / "train.txt")
    val_dataset = load_data(DATA_DIR / "val.txt")
    
    # Tokenize
    train_dataset = train_dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=["text"]
    )
    val_dataset = val_dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=["text"]
    )
    
    print(f"Train samples: {len(train_dataset)}")
    print(f"Val samples: {len(val_dataset)}")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        learning_rate=LEARNING_RATE,
        warmup_steps=100,
        logging_steps=10,
        save_steps=100,
        eval_steps=100,
        evaluation_strategy="steps",
        save_strategy="steps",
        save_total_limit=3,
        load_best_model_at_end=True,
        fp16=True,
        optim="paged_adamw_32bit",
        report_to="none"
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
    )
    
    print("Starting training...")
    trainer.train()
    
    print("Saving model...")
    # Save the fine-tuned model
    trainer.save_model(str(OUTPUT_DIR / "final_model"))
    tokenizer.save_pretrained(str(OUTPUT_DIR / "final_model"))
    
    print(f"Model saved to {OUTPUT_DIR / 'final_model'}")


if __name__ == "__main__":
    main()
