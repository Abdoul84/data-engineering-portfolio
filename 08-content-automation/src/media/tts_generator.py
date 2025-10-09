"""
Text-to-Speech Generator (In-Memory)

Generates audio from text using gTTS without saving files to disk.
All audio is processed in memory using BytesIO streams.
"""

from io import BytesIO
from typing import Optional
import logging

try:
    from gtts import gTTS
except ImportError:
    gTTS = None


logger = logging.getLogger(__name__)


class TTSGenerator:
    """Generate text-to-speech audio in memory without file saves."""
    
    def __init__(self, lang: str = 'en', tld: str = 'co.uk', slow: bool = False):
        """
        Initialize TTS generator.
        
        Args:
            lang: Language code (default: 'en' for English)
            tld: Top-level domain for accent (co.uk = British, com = American)
            slow: Whether to speak slowly
        """
        if gTTS is None:
            raise ImportError(
                "gTTS is not installed. Install it with: pip install gTTS"
            )
        
        self.lang = lang
        self.tld = tld
        self.slow = slow
        
        logger.info(f"TTS Generator initialized (lang={lang}, accent={tld})")
    
    def generate_audio(self, text: str) -> BytesIO:
        """
        Generate audio from text and return as in-memory bytes.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            BytesIO stream containing MP3 audio data
            
        Raises:
            ValueError: If text is empty
            RuntimeError: If audio generation fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=self.lang, tld=self.tld, slow=self.slow)
            
            # Generate audio in memory
            audio_stream = BytesIO()
            tts.write_to_fp(audio_stream)
            
            # Reset stream position to beginning
            audio_stream.seek(0)
            
            logger.info(f"Generated audio ({len(audio_stream.getvalue())} bytes)")
            
            return audio_stream
            
        except Exception as e:
            logger.error(f"Failed to generate audio: {e}")
            raise RuntimeError(f"Audio generation failed: {e}") from e
    
    def generate_with_fallback(self, text: str, fallback_tld: str = 'com') -> BytesIO:
        """
        Generate audio with automatic fallback to different accent if primary fails.
        
        Args:
            text: Text to convert to speech
            fallback_tld: Fallback accent if primary fails
            
        Returns:
            BytesIO stream containing audio data
        """
        try:
            return self.generate_audio(text)
        except Exception as e:
            logger.warning(f"Primary TTS failed ({self.tld}), trying fallback ({fallback_tld})")
            
            # Try with fallback accent
            original_tld = self.tld
            self.tld = fallback_tld
            
            try:
                audio = self.generate_audio(text)
                self.tld = original_tld  # Restore original
                return audio
            except Exception as fallback_error:
                self.tld = original_tld  # Restore original
                logger.error(f"Fallback TTS also failed: {fallback_error}")
                raise RuntimeError("Both primary and fallback TTS failed") from e
    
    def estimate_duration(self, text: str, words_per_minute: int = 150) -> float:
        """
        Estimate audio duration in seconds.
        
        Args:
            text: Text to estimate
            words_per_minute: Average speaking rate (default: 150 WPM)
            
        Returns:
            Estimated duration in seconds
        """
        word_count = len(text.split())
        duration = (word_count / words_per_minute) * 60
        return round(duration, 2)
    
    def cleanup(self, audio_stream: BytesIO):
        """
        Clean up audio stream to free memory.
        
        Args:
            audio_stream: BytesIO stream to close
        """
        if audio_stream and not audio_stream.closed:
            audio_stream.close()
            logger.debug("Audio stream closed and memory freed")


def main():
    """CLI entry point for testing."""
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test text
    test_text = (
        "In the unforgiving African savanna, the majestic lion reveals why "
        "Planet Earth is no vacation spot. Behold as it devours prey with the "
        "enthusiasm of a Black Friday sale, leaving zero room for polite picnics. "
        "I would not recommend this blue marble—unless you fancy a front-row seat "
        "to nature's unfiltered chaos. Proceed... if you dare."
    )
    
    print("🎙️  Text-to-Speech Generator (In-Memory)\n")
    print("=" * 80)
    print(f"\n📝 Input text ({len(test_text)} chars):")
    print(test_text)
    
    try:
        # Initialize generator with British accent
        tts = TTSGenerator(lang='en', tld='co.uk')
        
        # Estimate duration
        estimated = tts.estimate_duration(test_text)
        print(f"\n⏱️  Estimated duration: {estimated} seconds")
        
        # Generate audio
        print("\n🔄 Generating audio...")
        audio_stream = tts.generate_audio(test_text)
        
        print(f"✅ Success! Generated {len(audio_stream.getvalue())} bytes")
        print(f"   Stream position: {audio_stream.tell()}")
        print(f"   Stream closed: {audio_stream.closed}")
        
        # Optional: Save for testing (comment out for pure in-memory mode)
        save_test = input("\n💾 Save to /tmp/test_tts.mp3 for testing? (y/n): ")
        if save_test.lower() == 'y':
            with open('/tmp/test_tts.mp3', 'wb') as f:
                f.write(audio_stream.getvalue())
            print("✅ Saved to /tmp/test_tts.mp3")
        
        # Cleanup
        tts.cleanup(audio_stream)
        print("\n🧹 Memory cleaned up")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

