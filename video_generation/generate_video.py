import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
import argparse
from pathlib import Path
import imageio
import numpy as np


def load_svd_pipeline():
    """Load Stable Video Diffusion pipeline"""
    print("Loading Stable Video Diffusion pipeline...")
    
    pipeline = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt",
        torch_dtype=torch.float16,
        variant="fp16"
    )
    
    # Enable memory optimizations
    pipeline.enable_model_cpu_offload()
    
    return pipeline


def generate_video_from_image(
    pipeline,
    image_path: str,
    output_path: str,
    motion_bucket_id: int = 127,
    num_frames: int = 25,
    fps: int = 6
):
    """
    Generate video from a single image using SVD
    
    Args:
        pipeline: SVD pipeline
        image_path: Path to input image
        output_path: Path to save output video
        motion_bucket_id: Controls motion (1-255, higher = more motion)
        num_frames: Number of frames to generate
        fps: Frames per second for output
    """
    print(f"Generating video from {image_path}...")
    
    # Load image
    image = load_image(image_path)
    
    # Generate video
    with torch.no_grad():
        frames = pipeline(
            image,
            num_frames=num_frames,
            motion_bucket_id=motion_bucket_id,
            min_guidance_scale=1.0,
            max_guidance_scale=3.0,
        ).frames[0]
    
    # Save video
    export_to_video(frames, output_path, fps=fps)
    print(f"Video saved to {output_path}")
    
    return output_path


def generate_love_island_scene(
    pipeline,
    character_image: str,
    dialogue: str,
    scene_type: str = "confession",
    output_dir: str = "output"
):
    """
    Generate a Love Island scene video
    
    Args:
        pipeline: SVD pipeline
        character_image: Path to character image
        dialogue: Character's dialogue
        scene_type: Type of scene (confession, beach, villa, date)
        output_dir: Directory to save output
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Adjust motion based on scene type
    motion_settings = {
        "confession": 50,  # Low motion for talking head
        "beach": 150,      # Medium motion for beach scenes
        "villa": 100,      # Medium-low motion for villa
        "date": 180,       # Higher motion for date scenes
    }
    
    motion_bucket_id = motion_settings.get(scene_type, 127)
    
    # Generate video
    output_path = output_dir / f"{scene_type}_{Path(character_image).stem}.mp4"
    generate_video_from_image(
        pipeline,
        character_image,
        str(output_path),
        motion_bucket_id=motion_bucket_id,
        num_frames=25,
        fps=6
    )
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate videos using Stable Video Diffusion")
    parser.add_argument("--image", type=str, required=True, help="Path to input image")
    parser.add_argument("--output", type=str, default="output.mp4", help="Output video path")
    parser.add_argument("--motion", type=int, default=127, help="Motion bucket ID (1-255)")
    parser.add_argument("--frames", type=int, default=25, help="Number of frames")
    parser.add_argument("--fps", type=int, default=6, help="Frames per second")
    
    args = parser.parse_args()
    
    # Load pipeline
    pipeline = load_svd_pipeline()
    
    # Generate video
    generate_video_from_image(
        pipeline,
        args.image,
        args.output,
        motion_bucket_id=args.motion,
        num_frames=args.frames,
        fps=args.fps
    )


if __name__ == "__main__":
    main()
