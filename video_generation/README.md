# Text-to-Video Generation for Love Island

This module uses Stable Video Diffusion (SVD) to generate video clips from character images and dialogue.

## Setup

```bash
cd /home/asus/agentic-island/video_generation
pip install -r requirements.txt
```

## Usage

### Basic Usage

Generate a video from a single image:

```bash
python generate_video.py --image path/to/character.jpg --output output.mp4
```

### Parameters

- `--image`: Path to input character image (required)
- `--output`: Output video path (default: output.mp4)
- `--motion`: Motion bucket ID 1-255 (default: 127, higher = more motion)
- `--frames`: Number of frames to generate (default: 25)
- `--fps`: Frames per second (default: 6)

### Scene Types

Different scene types have different motion settings:

- **confession**: Low motion (50) - talking head style
- **beach**: Medium motion (150) - beach scenes
- **villa**: Medium-low motion (100) - villa scenes
- **date**: High motion (180) - date scenes

## Integration with Dialogue Generation

To generate videos for Love Island dialogue:

```python
from generate_video import load_svd_pipeline, generate_love_island_scene

# Load pipeline
pipeline = load_svd_pipeline()

# Generate confession scene
video_path = generate_love_island_scene(
    pipeline,
    character_image="path/to/kendall.jpg",
    dialogue="I can't believe he said that!",
    scene_type="confession",
    output_dir="output"
)
```

## Hardware Requirements

- GPU: NVIDIA GB10 (Blackwell) - supported
- VRAM: ~8GB recommended for SVD
- The script uses CPU offloading and VAE slicing for memory efficiency

## Next Steps

1. Generate character images from user photos
2. Create scene backgrounds (villa, beach, confession room)
3. Integrate with dialogue generation pipeline
4. Stitch multiple clips together for full episodes
