import json
from pathlib import Path
from typing import List, Dict
import random

INPUT_FILE = Path(__file__).parent.parent / "scrape" / "processed" / "training_data.jsonl"
OUTPUT_DIR = Path(__file__).parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

TRAIN_SPLIT = 0.8
VAL_SPLIT = 0.1
TEST_SPLIT = 0.1


def load_training_data(file_path: Path) -> List[Dict]:
    """Load training data from JSONL file"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def format_for_gemma(example: Dict) -> str:
    """Format example for Gemma fine-tuning"""
    # Gemma uses a specific format: <start_of_turn>user\n{instruction}\n<start_of_turn>model\n{output}<end_of_turn>
    instruction = example['instruction']
    input_text = example['input'] if example['input'] else ""
    output = example['output']
    
    # Combine instruction and input
    if input_text:
        user_message = f"{instruction}\n\nContext: {input_text}"
    else:
        user_message = instruction
    
    # Format for Gemma
    formatted = f"<start_of_turn>user\n{user_message}<end_of_turn>\n<start_of_turn>model\n{output}<end_of_turn>"
    return formatted


def split_data(data: List[Dict]) -> tuple[List[Dict], List[Dict], List[Dict]]:
    """Split data into train/val/test sets"""
    random.shuffle(data)
    
    total = len(data)
    train_end = int(total * TRAIN_SPLIT)
    val_end = train_end + int(total * VAL_SPLIT)
    
    train_data = data[:train_end]
    val_data = data[train_end:val_end]
    test_data = data[val_end:]
    
    return train_data, val_data, test_data


def save_split(data: List[Dict], output_path: Path):
    """Save data split to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for example in data:
            formatted = format_for_gemma(example)
            f.write(formatted + '\n')


def main():
    """Prepare data for Gemma fine-tuning"""
    print("Loading training data...")
    data = load_training_data(INPUT_FILE)
    print(f"Loaded {len(data)} examples")
    
    print("Splitting data...")
    train_data, val_data, test_data = split_data(data)
    print(f"Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")
    
    print("Saving formatted data...")
    save_split(train_data, OUTPUT_DIR / "train.txt")
    save_split(val_data, OUTPUT_DIR / "val.txt")
    save_split(test_data, OUTPUT_DIR / "test.txt")
    
    print(f"Data saved to {OUTPUT_DIR}")
    
    # Save metadata
    metadata = {
        "total_examples": len(data),
        "train_examples": len(train_data),
        "val_examples": len(val_data),
        "test_examples": len(test_data),
        "format": "gemma_instruction_tuning"
    }
    
    with open(OUTPUT_DIR / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("Metadata saved")
    
    # Show sample
    print("\nSample formatted example:")
    if train_data:
        sample = format_for_gemma(train_data[0])
        print(sample[:500] + "...")


if __name__ == "__main__":
    main()
