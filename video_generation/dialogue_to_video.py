import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
import edge_tts
import asyncio
try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
except ImportError:
    from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "finetune"))
from inference import load_model, generate_dialogue


class DialogueToVideoPipeline:
    """Pipeline to convert dialogue to video with audio"""
    
    def __init__(self):
        print("Initializing Dialogue-to-Video Pipeline...")
        self.video_pipeline = None
        self.tts = None
        self.gemma_model = None
        self.gemma_tokenizer = None
        
    def load_video_pipeline(self):
        """Load Stable Video Diffusion pipeline"""
        if self.video_pipeline is None:
            print("Loading Stable Video Diffusion pipeline...")
            self.video_pipeline = StableVideoDiffusionPipeline.from_pretrained(
                "stabilityai/stable-video-diffusion-img2vid-xt",
                torch_dtype=torch.float16,
                variant="fp16"
            )
            self.video_pipeline.enable_model_cpu_offload()
            print("Video pipeline loaded!")
    
    def load_tts(self):
        """Load Text-to-Speech model"""
        # edge-tts doesn't need loading, it's async
        print("Using edge-tts for audio generation...")
        self.tts = edge_tts
        print("TTS ready!")
    
    def load_gemma(self):
        """Load fine-tuned Gemma model"""
        if self.gemma_model is None:
            print("Loading fine-tuned Gemma model...")
            self.gemma_model, self.gemma_tokenizer = load_model()
            print("Gemma model loaded!")
    
    async def generate_audio(self, text: str, output_path: str, voice: str = "en-US-AriaNeural"):
        """Generate audio from text using edge-tts"""
        print(f"Generating audio for: {text[:50]}...")
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        
        print(f"Audio saved to {output_path}")
        return output_path
    
    def generate_video_clip(
        self,
        image_path: str,
        output_path: str,
        motion_bucket_id: int = 127,
        num_frames: int = 25,
        fps: int = 6
    ):
        """Generate video clip from image"""
        print(f"Generating video from {image_path}...")
        
        image = load_image(image_path)
        
        with torch.no_grad():
            frames = self.video_pipeline(
                image,
                num_frames=num_frames,
                motion_bucket_id=motion_bucket_id,
                min_guidance_scale=1.0,
                max_guidance_scale=3.0,
            ).frames[0]
        
        export_to_video(frames, output_path, fps=fps)
        print(f"Video saved to {output_path}")
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
            video = concatenate_videoclips(video_clips).subclipped(0, audio.duration)
        elif video.duration > audio.duration:
            video = video.subclipped(0, audio.duration)
        
        final_video = video.with_audio(audio)
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        print(f"Combined video saved to {output_path}")
        
        # Clean up temp files
        video.close()
        audio.close()
        
        return output_path
    
    async def generate_dialogue_clip(
        self,
        speaker: str,
        character_image: str,
        scene_type: str = "confession",
        output_dir: str = "output"
    ):
        """Generate a complete dialogue clip with video and audio"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # 1. Generate dialogue with Gemma
        dialogue = generate_dialogue(self.gemma_model, self.gemma_tokenizer, speaker)
        print(f"Generated dialogue: {dialogue[:100]}...")
        
        # 2. Generate video from character image
        motion_settings = {
            "confession": 50,
            "beach": 150,
            "villa": 100,
            "date": 180,
        }
        motion_bucket_id = motion_settings.get(scene_type, 127)
        
        video_path = output_dir / f"{speaker}_{scene_type}_video.mp4"
        self.generate_video_clip(
            character_image,
            str(video_path),
            motion_bucket_id=motion_bucket_id,
            num_frames=25,
            fps=6
        )
        
        # 3. Generate audio from dialogue
        audio_path = output_dir / f"{speaker}_{scene_type}_audio.wav"
        await self.generate_audio(dialogue, str(audio_path))
        
        # 4. Combine video and audio
        final_path = output_dir / f"{speaker}_{scene_type}_final.mp4"
        self.combine_video_audio(str(video_path), str(audio_path), str(final_path))
        
        return final_path, dialogue
    
    def generate_episode(
        self,
        speakers: list,
        character_images: dict,
        scene_type: str = "confession",
        output_dir: str = "output"
    ):
        """Generate a multi-speaker episode"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        clips = []
        dialogues = []
        
        for speaker in speakers:
            character_image = character_images.get(speaker)
            if not character_image:
                print(f"Warning: No image found for {speaker}, skipping...")
                continue
            
            clip_path, dialogue = self.generate_dialogue_clip(
                speaker,
                character_image,
                scene_type,
                output_dir
            )
            
            clips.append(clip_path)
            dialogues.append((speaker, dialogue))
        
        # Stitch all clips together
        if len(clips) > 1:
            print("Stitching clips together...")
            video_clips = [VideoFileClip(str(clip)) for clip in clips]
            final_episode = concatenate_videoclips(video_clips)
            episode_path = output_dir / f"episode_{scene_type}.mp4"
            final_episode.write_videofile(str(episode_path), codec='libx264')
            
            # Clean up
            for clip in video_clips:
                clip.close()
            
            print(f"Episode saved to {episode_path}")
            return episode_path, dialogues
        elif len(clips) == 1:
            return clips[0], dialogues
        else:
            return None, dialogues


async def main():
    """Example usage"""
    pipeline = DialogueToVideoPipeline()
    
    # Load all models
    pipeline.load_video_pipeline()
    pipeline.load_tts()
    pipeline.load_gemma()
    
    # Example: Generate dialogue clip for a single speaker
    print("\n=== Generating Single Dialogue Clip ===")
    clip_path, dialogue = await pipeline.generate_dialogue_clip(
        speaker="Kendall",
        character_image="/home/asus/agentic-island/test.jpg",
        scene_type="confession",
        output_dir="output"
    )
    
    print(f"\nClip generated: {clip_path}")
    print(f"Dialogue: {dialogue}")


if __name__ == "__main__":
    asyncio.run(main())
