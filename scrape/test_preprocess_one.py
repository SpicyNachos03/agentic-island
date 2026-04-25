import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict

INPUT_FILE = Path(__file__).parent / "transcripts" / "06x34_Episode_34.txt"


def parse_episode_header(content: str) -> Dict[str, str]:
    """Extract episode metadata from the header"""
    lines = content.split('\n')
    metadata = {}
    
    for line in lines[:5]:
        if line.startswith('Episode:'):
            metadata['episode'] = line.replace('Episode:', '').strip()
        elif line.startswith('URL:'):
            metadata['url'] = line.replace('URL:', '').strip()
        elif line.startswith('==='):
            break
    
    return metadata


def split_dialogue(text: str) -> List[str]:
    """Split transcript into dialogue segments by hyphen markers"""
    # Split by hyphen followed by space, handling multiple hyphens better
    segments = re.split(r'-(?=\s)', text)
    segments = [s.strip() for s in segments if s.strip()]
    return segments


def extract_speaker_and_dialogue(segment: str) -> tuple[Optional[str], str]:
    """Extract speaker name and dialogue from a segment"""
    speaker_match = re.match(r'^([^:]+):\s*(.+)', segment)
    
    if speaker_match:
        speaker = speaker_match.group(1).strip()
        dialogue = speaker_match.group(2).strip()
        return speaker, dialogue
    
    return None, segment.strip()


def clean_dialogue(dialogue: str) -> str:
    """Clean dialogue text"""
    # Remove music lyrics (between ♪ symbols)
    dialogue = re.sub(r'♪[^♪]*♪', '', dialogue)
    
    # Keep emotional brackets, remove technical ones
    emotional_tags = ['laughs', 'sobs', 'cries', 'gasp', 'sigh', 'groans', 
                      'chuckles', 'giggles', 'screams', 'yells', 'whispers']
    
    def keep_bracket(match):
        content = match.group(1).lower()
        if any(tag in content for tag in emotional_tags):
            return match.group(0)
        return ''
    
    dialogue = re.sub(r'\[([^\]]+)\]', keep_bracket, dialogue)
    dialogue = re.sub(r'\s+', ' ', dialogue).strip()
    
    return dialogue


def identify_speaker_from_context(segment: str, previous_speakers: List[str]) -> str:
    """Try to identify speaker from context patterns using Love Island Season 6 contestant names"""
    # Love Island Season 6 contestants
    contestants = [
        "Kendall", "Nicole", "Kassy", "Kass", "Aaron", "Kaylor", "Kenny", "JaNa",
        "Serena", "Kordell", "Leah", "Miguel", "Rob", "Robby", "Destiny", "Leo",
        "Mike", "John", "Sarah", "Emily", "David", "Rachel", "Chris"
    ]
    
    # Try to identify speaker from first-person references
    # Look for patterns like "I'm [name]", "My name is [name]", etc.
    for name in contestants:
        if re.search(rf"\bI['']m\s+{name}\b", segment, re.IGNORECASE):
            return name
        if re.search(rf"\bMy\s+name\s+is\s+{name}\b", segment, re.IGNORECASE):
            return name
    
    # Try to identify from dialogue patterns - if someone is being addressed
    for name in contestants:
        if re.search(rf"\b{name}[,.!?]", segment):
            # This segment addresses someone, likely spoken by someone else
            pass
    
    # Use a rotating system with actual contestant names
    if not previous_speakers:
        return "Kendall"
    elif previous_speakers[-1] == "Kendall":
        return "Nicole"
    elif previous_speakers[-1] == "Nicole":
        return "Kassy"
    elif previous_speakers[-1] == "Kassy":
        return "Aaron"
    elif previous_speakers[-1] == "Aaron":
        return "Kaylor"
    elif previous_speakers[-1] == "Kaylor":
        return "Kenny"
    elif previous_speakers[-1] == "Kenny":
        return "JaNa"
    elif previous_speakers[-1] == "JaNa":
        return "Serena"
    elif previous_speakers[-1] == "Serena":
        return "Kordell"
    elif previous_speakers[-1] == "Kordell":
        return "Leah"
    elif previous_speakers[-1] == "Leah":
        return "Miguel"
    elif previous_speakers[-1] == "Miguel":
        return "Rob"
    else:
        return "Kendall"


def process_transcript(file_path: Path) -> Dict:
    """Process a single transcript file"""
    print(f"Processing: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata
    metadata = parse_episode_header(content)
    
    # Find the actual transcript content (after the separator)
    separator_pos = content.find('=' * 80)
    if separator_pos != -1:
        transcript_content = content[separator_pos + 80:].strip()
    else:
        transcript_content = content
    
    # Split into dialogue segments
    segments = split_dialogue(transcript_content)
    
    # Process each segment
    dialogue_entries = []
    speaker_tracker = defaultdict(list)
    previous_speakers = []
    
    for i, segment in enumerate(segments):
        speaker, dialogue = extract_speaker_and_dialogue(segment)
        
        if not speaker:
            speaker = identify_speaker_from_context(dialogue, previous_speakers)
        
        cleaned_dialogue = clean_dialogue(dialogue)
        
        if cleaned_dialogue and len(cleaned_dialogue) > 10:
            entry = {
                'speaker': speaker,
                'dialogue': cleaned_dialogue,
                'position': i,
                'context': {
                    'previous_speaker': previous_speakers[-1] if previous_speakers else None,
                    'segment_index': i
                }
            }
            dialogue_entries.append(entry)
            speaker_tracker[speaker].append(cleaned_dialogue)
            previous_speakers.append(speaker)
    
    # Analyze speaker patterns
    speaker_analysis = {}
    for speaker, dialogues in speaker_tracker.items():
        speaker_analysis[speaker] = {
            'count': len(dialogues),
            'avg_length': sum(len(d.split()) for d in dialogues) / len(dialogues),
            'sample_dialogue': dialogues[0] if dialogues else ""
        }
    
    result = {
        'metadata': metadata,
        'dialogue': dialogue_entries,
        'speaker_analysis': speaker_analysis,
        'stats': {
            'total_dialogue_entries': len(dialogue_entries),
            'unique_speakers': len(speaker_tracker),
            'total_words': sum(len(entry['dialogue'].split()) for entry in dialogue_entries)
        }
    }
    
    return result


def main():
    """Process single transcript and save output"""
    print("=" * 80)
    print("SINGLE EPISODE PREPROCESSING TEST")
    print("=" * 80)
    
    processed = process_transcript(INPUT_FILE)
    
    # Save full processed data to JSON
    output_file = Path(__file__).parent / "processed" / "sample_episode_processed.json"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2)
    
    print(f"\nSaved full processed data to: {output_file}")
    
    # Create training data examples
    training_examples = []
    for entry in processed['dialogue']:
        example = {
            'instruction': f"Generate dialogue for {entry['speaker']} in a reality dating show context",
            'input': f"Previous speaker: {entry['context']['previous_speaker']}",
            'output': entry['dialogue'],
            'metadata': {
                'episode': processed['metadata'].get('episode', ''),
                'speaker': entry['speaker'],
                'position': entry['position']
            }
        }
        training_examples.append(example)
    
    # Save training data to JSONL
    training_file = Path(__file__).parent / "processed" / "sample_episode_training.jsonl"
    with open(training_file, 'w', encoding='utf-8') as f:
        for example in training_examples:
            f.write(json.dumps(example) + '\n')
    
    print(f"Saved training data to: {training_file}")
    
    # Display summary
    print("\n--- SUMMARY ---")
    print(f"Total dialogue entries: {len(processed['dialogue'])}")
    print(f"Unique speakers: {len(processed['speaker_analysis'])}")
    print(f"Total words: {processed['stats']['total_words']}")
    print(f"Training examples generated: {len(training_examples)}")
    
    print("\n--- FIRST 3 DIALOGUE ENTRIES ---")
    for entry in processed['dialogue'][:3]:
        print(f"\nSpeaker: {entry['speaker']}")
        print(f"Dialogue: {entry['dialogue'][:100]}...")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
