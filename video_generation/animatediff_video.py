import torch
from diffusers import AnimateDiffPipeline, DDIMScheduler, MotionAdapter
from diffusers.utils import export_to_video
import edge_tts
import asyncio
try:
    from moviepy.editor import VideoFileClip, AudioFileClip
except ImportError:
    from moviepy import VideoFileClip, AudioFileClip
from pathlib import Path
from PIL import Image
import numpy as np


class AnimateDiffVideoGenerator:
    """Generate videos with AnimateDiff for better text control"""
    
    def __init__(self):
        print("Initializing AnimateDiff Video Generator...")
        self.pipeline = None
        self.tts = edge_tts
        
    def load_pipeline(self):
        """Load AnimateDiff pipeline"""
        if self.pipeline is None:
            print("Loading AnimateDiff pipeline...")
            
            # Load motion adapter
            adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2")
            
            # Load base pipeline (using Stable Diffusion as base)
            from diffusers import StableDiffusionPipeline
            base = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16,
                variant="fp16"
            )
            
            # Create AnimateDiff pipeline
            self.pipeline = AnimateDiffPipeline(
                vae=base.vae,
                text_encoder=base.text_encoder,
                tokenizer=base.tokenizer,
                unet=base.unet,
                motion_adapter=adapter,
                scheduler=DDIMScheduler.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    subfolder="scheduler"
                )
            )
            
            # Enable memory optimizations
            self.pipeline.enable_model_cpu_offload()
            self.pipeline.enable_vae_slicing()
            
            print("AnimateDiff pipeline loaded!")
    
    async def generate_video_from_text(
        self,
        prompt: str,
        output_path: str = "output.mp4",
        negative_prompt: str = "bad quality, worse quality, low resolution",
        image_path: str = None,
        num_frames: int = 16,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 25
    ):
        """
        Generate video from text prompt with optional image reference
        
        Args:
            prompt: Text description of the video
            negative_prompt: Things to avoid in generation
            image_path: Optional reference image for character
            num_frames: Number of frames to generate
            guidance_scale: How closely to follow prompt
            num_inference_steps: Number of denoising steps
            output_path: Where to save the video
        """
        print(f"Generating video for prompt: {prompt[:100]}...")
        
        # Load reference image if provided
        reference_image = None
        if image_path:
            reference_image = Image.open(image_path).convert("RGB")
            reference_image = reference_image.resize((512, 512))
        
        # Generate video
        with torch.no_grad():
            if reference_image:
                # Image-to-video with text guidance
                output = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=reference_image,
                    num_frames=num_frames,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    generator=torch.Generator("cuda").manual_seed(42)
                )
            else:
                # Pure text-to-video
                output = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_frames=num_frames,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    generator=torch.Generator("cuda").manual_seed(42)
                )
        
        frames = output.frames[0]
        export_to_video(frames, output_path, fps=8)
        
        print(f"Video saved to {output_path}")
        return output_path
    
    async def generate_audio(self, text: str, output_path: str, voice: str = "en-US-AriaNeural"):
        """Generate audio from text using edge-tts"""
        print(f"Generating audio for: {text[:50]}...")
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        
        print(f"Audio saved to {output_path}")
        return output_path
    
    def combine_video_audio(self, video_path: str, audio_path: str, output_path: str):
        """Combine video and audio"""
        print(f"Combining video and audio...")
        
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Loop video to match audio duration if needed
        if video.duration < audio.duration:
            # Manually loop by concatenating for moviepy 2.x
            loops_needed = int(audio.duration / video.duration) + 1
            video_clips = [video] * loops_needed
            from moviepy import concatenate_videoclips
            video = concatenate_videoclips(video_clips).subclipped(0, audio.duration)
        elif video.duration > audio.duration:
            video = video.subclipped(0, audio.duration)
        
        final_video = video.with_audio(audio)
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        print(f"Combined video saved to {output_path}")
        
        # Clean up
        video.close()
        audio.close()
        
        return output_path
    
    async def generate_love_island_clip(
        self,
        speaker: str,
        dialogue: str,
        character_image: str,
        scene_type: str = "confession",
        output_dir: str = "output"
    ):
        """
        Generate a Love Island clip with character action based on dialogue
        
        Args:
            speaker: Character name
            dialogue: What the character says
            character_image: Path to character image
            scene_type: Type of scene (confession, beach, villa, date)
            output_dir: Output directory
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Create action prompt based on dialogue content
        action_prompts = {
            "confession": f"{speaker} talking to camera, intimate confession, emotional expression, looking at camera",
            "beach": f"{speaker} walking on beach, relaxed, enjoying sun, casual movement",
            "villa": f"{speaker} in villa, socializing, interacting with others, lively atmosphere",
            "date": f"{speaker} on romantic date, intimate moments, romantic gestures, smiling"
        }
        
        base_prompt = action_prompts.get(scene_type, f"{speaker} talking")
        
        # Add dialogue context to prompt
        prompt = f"{base_prompt}, saying: {dialogue[:50]}..., high quality, detailed"
        
        # Generate video
        video_path = output_dir / f"{speaker}_{scene_type}_animatediff.mp4"
        await self.generate_video_from_text(
            prompt=prompt,
            image_path=character_image,
            num_frames=16,
            guidance_scale=7.5,
            output_path=str(video_path)
        )
        
        # Generate audio
        audio_path = output_dir / f"{speaker}_{scene_type}_audio.wav"
        await self.generate_audio(dialogue, str(audio_path))
        
        # Combine
        final_path = output_dir / f"{speaker}_{scene_type}_final.mp4"
        self.combine_video_audio(str(video_path), str(audio_path), str(final_path))
        
        return final_path


async def main():
    """Example usage"""
    generator = AnimateDiffVideoGenerator()
    
    # Load pipeline
    generator.load_pipeline()
    
    # Example: Generate video with text control
    print("\n=== Generating Video with Text Control ===")
    
    clip_path = await generator.generate_love_island_clip(
        speaker="Kendall",
        dialogue="I can't believe he said that to me. I'm so hurt right now.",
        character_image="/home/asus/agentic-island/test.jpg",
        scene_type="confession",
        output_dir="output"
    )
    
    print(f"\nClip generated: {clip_path}")


if __name__ == "__main__":
    asyncio.run(main())
