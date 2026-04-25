import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict

INPUT_DIR = Path(__file__).parent / "transcripts"
OUTPUT_DIR = Path(__file__).parent / "processed"
OUTPUT_DIR.mkdir(exist_ok=True)


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
    # Clean up segments
    segments = [s.strip() for s in segments if s.strip()]
    return segments


def extract_speaker_and_dialogue(segment: str) -> tuple[Optional[str], str]:
    """Extract speaker name and dialogue from a segment"""
    # Try to match pattern: "Speaker: Dialogue"
    speaker_match = re.match(r'^([^:]+):\s*(.+)', segment)
    
    if speaker_match:
        speaker = speaker_match.group(1).strip()
        dialogue = speaker_match.group(2).strip()
        return speaker, dialogue
    
    # If no speaker found, return None
    return None, segment.strip()


def clean_dialogue(dialogue: str) -> str:
    """Clean dialogue text"""
    # Remove music lyrics (between ♪ symbols)
    dialogue = re.sub(r'♪[^♪]*♪', '', dialogue)
    
    # Remove sound effects in brackets but keep emotional context
    # Keep emotional brackets like [Laughs], [Sobs], remove technical ones
    emotional_tags = ['laughs', 'sobs', 'cries', 'gasp', 'sigh', 'groans', 
                      'chuckles', 'giggles', 'screams', 'yells', 'whispers']
    
    def keep_bracket(match):
        content = match.group(1).lower()
        if any(tag in content for tag in emotional_tags):
            return match.group(0)  # Keep emotional tags
        return ''  # Remove technical tags
    
    dialogue = re.sub(r'\[([^\]]+)\]', keep_bracket, dialogue)
    
    # Clean up extra whitespace
    dialogue = re.sub(r'\s+', ' ', dialogue).strip()
    
    # Remove trailing punctuation issues
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
        
        if cleaned_dialogue and len(cleaned_dialogue) > 10:  # Filter out very short segments
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


def extract_character_relationships(dialogue_entries: List[Dict]) -> Dict:
    """Extract character relationships from dialogue patterns"""
    relationships = defaultdict(lambda: {'mentions': 0, 'interactions': 0})
    
    for i, entry in enumerate(dialogue_entries):
        current_speaker = entry['speaker']
        dialogue = entry['dialogue'].lower()
        
        # Look for name mentions (common Love Island names)
        common_names = ['kendall', 'nicole', 'destiny', 'leo', 'kassy', 'mike', 
                       'john', 'sarah', 'emily', 'david', 'rachel', 'chris']
        
        for name in common_names:
            if name in dialogue and name != current_speaker.lower():
                relationships[(current_speaker, name)]['mentions'] += 1
        
        # Track consecutive speakers as interactions
        if i > 0:
            prev_speaker = dialogue_entries[i-1]['speaker']
            if prev_speaker != current_speaker:
                relationships[(prev_speaker, current_speaker)]['interactions'] += 1
    
    return dict(relationships)


def create_training_format(processed_data: Dict) -> List[Dict]:
    """Convert processed data to training format for Gemma"""
    training_examples = []
    
    for entry in processed_data['dialogue']:
        # Create instruction-response pairs
        example = {
            'instruction': f"Generate dialogue for {entry['speaker']} in a reality dating show context",
            'input': f"Previous speaker: {entry['context']['previous_speaker']}",
            'output': entry['dialogue'],
            'metadata': {
                'episode': processed_data['metadata'].get('episode', ''),
                'speaker': entry['speaker'],
                'position': entry['position']
            }
        }
        training_examples.append(example)
    
    return training_examples


def main():
    """Process all transcript files"""
    print("Starting transcript preprocessing...")
    
    # Get all transcript files
    transcript_files = list(INPUT_DIR.glob("*.txt"))
    print(f"Found {len(transcript_files)} transcript files")
    
    all_processed = []
    all_training_data = []
    
    for file_path in transcript_files:
        try:
            processed = process_transcript(file_path)
            all_processed.append(processed)
            
            # Create training format
            training_data = create_training_format(processed)
            all_training_data.extend(training_data)
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            continue
    
    # Save processed data
    output_file = OUTPUT_DIR / "processed_transcripts.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_processed, f, indent=2)
    print(f"Saved processed data to: {output_file}")
    
    # Save training data
    training_file = OUTPUT_DIR / "training_data.jsonl"
    with open(training_file, 'w', encoding='utf-8') as f:
        for example in all_training_data:
            f.write(json.dumps(example) + '\n')
    print(f"Saved training data to: {training_file}")
    
    # Print summary
    print("\n=== Processing Summary ===")
    print(f"Total episodes processed: {len(all_processed)}")
    print(f"Total dialogue entries: {sum(p['stats']['total_dialogue_entries'] for p in all_processed)}")
    print(f"Total training examples: {len(all_training_data)}")
    
    # Speaker statistics
    all_speakers = defaultdict(int)
    for processed in all_processed:
        for speaker, data in processed['speaker_analysis'].items():
            all_speakers[speaker] += data['count']
    
    print(f"\nTop speakers by dialogue count:")
    for speaker, count in sorted(all_speakers.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {speaker}: {count} dialogues")


if __name__ == "__main__":
    main()
