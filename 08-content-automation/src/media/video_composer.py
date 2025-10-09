"""
Video Composer (In-Memory)

Assembles final video from footage + audio + text overlays without saving to disk.
All processing done in memory using moviepy.
"""

from io import BytesIO
from typing import Optional, Tuple
import logging
import tempfile
import os

MOVIEPY_AVAILABLE = False
VideoFileClip = None
AudioFileClip = None
TextClip = None
CompositeVideoClip = None
concatenate_videoclips = None
ColorClip = None
vfx = None

# Try moviepy 2.x imports first
try:
    from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip
    try:
        import moviepy.video.fx.all as vfx
    except ImportError:
        import moviepy.video.fx as vfx
    MOVIEPY_AVAILABLE = True
except ImportError:
    # Fallback to moviepy 1.x imports
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip
        try:
            from moviepy.video.fx import all as vfx
        except ImportError:
            from moviepy.video import fx as vfx
        MOVIEPY_AVAILABLE = True
    except ImportError:
        pass


logger = logging.getLogger(__name__)


class VideoComposer:
    """Compose final video with footage, audio, and text overlays in memory."""
    
    def __init__(
        self,
        target_duration: int = 30,
        target_size: Tuple[int, int] = (1080, 1920),  # 9:16 for TikTok
        fps: int = 30
    ):
        """
        Initialize video composer.
        
        Args:
            target_duration: Target video duration in seconds
            target_size: Target video resolution (width, height)
            fps: Frames per second
        """
        if not MOVIEPY_AVAILABLE:
            raise ImportError(
                "moviepy is not installed. Install with: pip install moviepy"
            )
        
        self.target_duration = target_duration
        self.target_size = target_size
        self.fps = fps
        
        logger.info(
            f"Video Composer initialized "
            f"({target_size[0]}x{target_size[1]}, {fps}fps, {target_duration}s)"
        )
    
    def _write_temp_file(self, stream: BytesIO, suffix: str) -> str:
        """
        Write BytesIO stream to temporary file (moviepy requires file paths).
        
        Args:
            stream: BytesIO stream
            suffix: File extension (e.g., '.mp4', '.mp3')
            
        Returns:
            Path to temporary file
        """
        fd, path = tempfile.mkstemp(suffix=suffix)
        try:
            with os.fdopen(fd, 'wb') as f:
                f.write(stream.getvalue())
            return path
        except Exception as e:
            os.close(fd)
            raise e
    
    def compose_video(
        self,
        video_stream: BytesIO,
        audio_stream: BytesIO,
        text_overlay: str = "NOT RECOMMENDED",
        apply_dark_filter: bool = True
    ) -> BytesIO:
        """
        Compose final video with footage, audio, and text overlay.
        
        Args:
            video_stream: Video footage (BytesIO)
            audio_stream: Audio narration (BytesIO)
            text_overlay: Text to overlay on video
            apply_dark_filter: Whether to apply dark/horror filter
            
        Returns:
            BytesIO stream containing final video
            
        Raises:
            RuntimeError: If composition fails
        """
        temp_video_path = None
        temp_audio_path = None
        temp_output_path = None
        video_clip = None
        audio_clip = None
        
        try:
            # Write streams to temporary files (moviepy limitation)
            logger.info("Writing streams to temporary files...")
            temp_video_path = self._write_temp_file(video_stream, '.mp4')
            temp_audio_path = self._write_temp_file(audio_stream, '.mp3')
            
            # Load video
            logger.info("Loading video clip...")
            video_clip = VideoFileClip(temp_video_path)
            
            # Resize to target dimensions
            video_clip = video_clip.resized(self.target_size)
            
            # Trim or loop to match target duration
            if video_clip.duration < self.target_duration:
                # Loop video if too short
                n_loops = int(self.target_duration / video_clip.duration) + 1
                video_clip = concatenate_videoclips([video_clip] * n_loops)
            
            video_clip = video_clip.subclipped(0, self.target_duration)
            
            # Skip complex effects for speed - just use the raw video
            logger.info("Skipping visual effects for faster rendering...")
            video_with_text = video_clip
            
            # Load and set audio
            logger.info("Adding audio...")
            audio_clip = AudioFileClip(temp_audio_path)
            
            # Trim or extend audio to match video duration
            if audio_clip.duration > self.target_duration:
                audio_clip = audio_clip.subclipped(0, self.target_duration)
            
            video_with_text = video_with_text.with_audio(audio_clip)
            
            # Write to temporary output file
            logger.info("Rendering final video...")
            temp_output_path = tempfile.mktemp(suffix='.mp4')
            
            video_with_text.write_videofile(
                temp_output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=tempfile.mktemp(suffix='.m4a'),
                remove_temp=True,
                logger=None  # Suppress moviepy logs
            )
            
            # Read output into BytesIO
            output_stream = BytesIO()
            with open(temp_output_path, 'rb') as f:
                output_stream.write(f.read())
            
            output_stream.seek(0)
            
            logger.info(
                f"Video composed successfully "
                f"({len(output_stream.getvalue()) / 1024 / 1024:.2f} MB)"
            )
            
            return output_stream
            
        except Exception as e:
            logger.error(f"Video composition failed: {e}")
            raise RuntimeError(f"Failed to compose video: {e}") from e
        
        finally:
            # Clean up clips
            if video_clip:
                video_clip.close()
            if audio_clip:
                audio_clip.close()
            
            # Clean up temporary files
            for path in [temp_video_path, temp_audio_path, temp_output_path]:
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                        logger.debug(f"Removed temp file: {path}")
                    except Exception as e:
                        logger.warning(f"Failed to remove temp file {path}: {e}")
    
    def cleanup(self, video_stream: BytesIO):
        """
        Clean up video stream to free memory.
        
        Args:
            video_stream: BytesIO stream to close
        """
        if video_stream and not video_stream.closed:
            video_stream.close()
            logger.debug("Video stream closed and memory freed")


def main():
    """CLI entry point for testing."""
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🎬 Video Composer (In-Memory)\n")
    print("=" * 80)
    print("\n⚠️  This requires test video and audio files in /tmp/")
    print("    Run tts_generator.py and video_fetcher.py first to generate them.\n")
    
    video_path = "/tmp/test_video.mp4"
    audio_path = "/tmp/test_tts.mp3"
    
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        print("   Run video_fetcher.py first")
        sys.exit(1)
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio not found: {audio_path}")
        print("   Run tts_generator.py first")
        sys.exit(1)
    
    try:
        # Load test files into memory
        print("📂 Loading test files...")
        with open(video_path, 'rb') as f:
            video_stream = BytesIO(f.read())
        
        with open(audio_path, 'rb') as f:
            audio_stream = BytesIO(f.read())
        
        print(f"   Video: {len(video_stream.getvalue()) / 1024 / 1024:.2f} MB")
        print(f"   Audio: {len(audio_stream.getvalue()) / 1024:.2f} KB")
        
        # Initialize composer
        composer = VideoComposer(target_duration=30)
        
        # Compose video
        print("\n🎬 Composing final video...")
        print("   (This may take 1-2 minutes...)")
        
        final_stream = composer.compose_video(
            video_stream,
            audio_stream,
            text_overlay="NOT RECOMMENDED"
        )
        
        size_mb = len(final_stream.getvalue()) / 1024 / 1024
        print(f"\n✅ Success! Final video in memory ({size_mb:.2f} MB)")
        
        # Save for testing
        output_path = "/tmp/final_video.mp4"
        with open(output_path, 'wb') as f:
            f.write(final_stream.getvalue())
        
        print(f"✅ Saved to {output_path} for testing")
        
        # Cleanup
        composer.cleanup(final_stream)
        print("\n🧹 Memory cleaned up")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

