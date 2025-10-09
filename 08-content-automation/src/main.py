"""
Planet Earth Parody Pipeline - Main Orchestrator

Chains all components together:
1. Generate script
2. Create TTS audio (in-memory)
3. Fetch stock footage (in-memory)
4. Compose video (in-memory)
5. Upload to TikTok

Zero local storage - everything streams through RAM.
"""

import sys
import logging
from datetime import datetime, timezone
from typing import Dict, Optional
import json
import yaml
from pathlib import Path

# Import pipeline components
from .generation.planet_earth_generator import PlanetEarthGenerator
from .media.tts_generator import TTSGenerator
from .media.video_fetcher import VideoFetcher
from .media.video_composer import VideoComposer
from .posting.tiktok_uploader import TikTokUploader


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class PlanetEarthPipeline:
    """Main pipeline orchestrator for automated content generation."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize pipeline with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        logger.info("Initializing Planet Earth Parody Pipeline...")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.generator = PlanetEarthGenerator()
        self.tts = TTSGenerator(lang='en', tld='co.uk')  # British accent
        
        # Initialize video fetcher (requires API key)
        pexels_key = self.config.get('pexels', {}).get('api_key')
        if pexels_key and pexels_key != 'YOUR_PEXELS_API_KEY':
            self.video_fetcher = VideoFetcher(pexels_key)
        else:
            logger.warning("No valid Pexels API key - video fetching will be skipped")
            self.video_fetcher = None
        
        # Initialize video composer
        video_duration = self.config.get('content', {}).get('video_duration', 30)
        self.composer = VideoComposer(target_duration=video_duration)
        
        # Initialize uploader
        tiktok_token = self.config.get('tiktok', {}).get('access_token')
        dry_run = self.config.get('processing', {}).get('dry_run', True)
        self.uploader = TikTokUploader(access_token=tiktok_token, dry_run=dry_run)
        
        logger.info("Pipeline initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return {}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def run(self, save_output: bool = False) -> Dict:
        """
        Run the complete pipeline.
        
        Args:
            save_output: If True, save final video to /tmp for testing
            
        Returns:
            Dict with pipeline execution results
        """
        logger.info("=" * 80)
        logger.info("Starting Planet Earth Parody Pipeline")
        logger.info("=" * 80)
        
        result = {
            'success': False,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'stages': {}
        }
        
        try:
            # Stage 1: Generate content
            logger.info("\n[1/5] 📝 Generating script...")
            content = self.generator.generate_content()
            result['stages']['generation'] = {
                'success': True,
                'animal': content['animal'],
                'location': content['location']
            }
            logger.info(f"✅ Generated: {content['animal']} in {content['location']}")
            
            # Stage 2: Generate TTS audio
            logger.info("\n[2/5] 🎙️  Generating voiceover...")
            audio_stream = self.tts.generate_audio(content['script'])
            audio_size_kb = len(audio_stream.getvalue()) / 1024
            result['stages']['tts'] = {
                'success': True,
                'size_kb': round(audio_size_kb, 2)
            }
            logger.info(f"✅ Audio generated: {audio_size_kb:.2f} KB")
            
            # Stage 3: Fetch video footage
            if self.video_fetcher:
                logger.info("\n[3/5] 🎬 Fetching stock footage...")
                video_stream = self.video_fetcher.fetch_video(
                    content['animal'],
                    content['location']
                )
                
                if video_stream:
                    video_size_mb = len(video_stream.getvalue()) / 1024 / 1024
                    result['stages']['video_fetch'] = {
                        'success': True,
                        'size_mb': round(video_size_mb, 2)
                    }
                    logger.info(f"✅ Video fetched: {video_size_mb:.2f} MB")
                else:
                    logger.error("❌ Failed to fetch video")
                    result['stages']['video_fetch'] = {'success': False}
                    return result
            else:
                logger.warning("⚠️  [3/5] Video fetching skipped (no API key)")
                result['stages']['video_fetch'] = {'success': False, 'skipped': True}
                return result
            
            # Stage 4: Compose final video
            logger.info("\n[4/5] 🎬 Composing final video...")
            logger.info("   (This may take 1-2 minutes...)")
            
            final_stream = self.composer.compose_video(
                video_stream,
                audio_stream,
                text_overlay="NOT RECOMMENDED",
                apply_dark_filter=True
            )
            
            final_size_mb = len(final_stream.getvalue()) / 1024 / 1024
            result['stages']['composition'] = {
                'success': True,
                'size_mb': round(final_size_mb, 2)
            }
            logger.info(f"✅ Video composed: {final_size_mb:.2f} MB")
            
            # Optional: Save for testing
            if save_output:
                output_path = f"/tmp/planet_earth_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                self.uploader.save_to_file(final_stream, output_path)
                result['output_file'] = output_path
                logger.info(f"💾 Saved to: {output_path}")
                # Reset stream position after saving
                final_stream.seek(0)
            
            # Stage 5: Upload to TikTok
            logger.info("\n[5/5] 📤 Uploading to TikTok...")
            
            upload_result = self.uploader.upload_video(
                final_stream,
                caption=content['caption'],
                hashtags=None,  # Already in caption
                privacy="public"
            )
            
            result['stages']['upload'] = upload_result
            
            if upload_result.get('success'):
                logger.info(f"✅ Upload successful")
                if upload_result.get('dry_run'):
                    logger.info("   (DRY RUN MODE - no actual post)")
                else:
                    logger.info(f"   Post URL: {upload_result.get('post_url')}")
            else:
                logger.error(f"❌ Upload failed: {upload_result.get('error')}")
            
            # Cleanup memory
            logger.info("\n🧹 Cleaning up memory...")
            self.tts.cleanup(audio_stream)
            self.video_fetcher.cleanup(video_stream) if self.video_fetcher else None
            self.composer.cleanup(final_stream)
            logger.info("✅ Memory cleaned")
            
            # Overall success
            result['success'] = all(
                stage.get('success', False) 
                for stage in result['stages'].values()
            )
            
            return result
            
        except Exception as e:
            logger.error(f"\n❌ Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            result['error'] = str(e)
            return result
        
        finally:
            logger.info("\n" + "=" * 80)
            logger.info("Pipeline execution completed")
            logger.info("=" * 80)
    
    def run_batch(self, count: int = 1) -> list:
        """
        Run pipeline multiple times.
        
        Args:
            count: Number of videos to generate
            
        Returns:
            List of results
        """
        results = []
        
        for i in range(count):
            logger.info(f"\n\n{'#' * 80}")
            logger.info(f"Batch {i+1}/{count}")
            logger.info(f"{'#' * 80}\n")
            
            result = self.run()
            results.append(result)
            
            if not result['success']:
                logger.warning(f"Batch {i+1} failed, stopping")
                break
        
        return results


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Planet Earth Parody - Automated Content Pipeline'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save output video to /tmp for testing'
    )
    parser.add_argument(
        '--batch',
        type=int,
        default=1,
        help='Number of videos to generate'
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = PlanetEarthPipeline(config_path=args.config)
    
    # Run pipeline
    if args.batch > 1:
        results = pipeline.run_batch(count=args.batch)
        
        # Print summary
        print("\n\n" + "=" * 80)
        print("BATCH EXECUTION SUMMARY")
        print("=" * 80)
        
        successful = sum(1 for r in results if r['success'])
        print(f"Total: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {len(results) - successful}")
        
    else:
        result = pipeline.run(save_output=args.save)
        
        # Print result
        print("\n\n" + "=" * 80)
        print("EXECUTION RESULT")
        print("=" * 80)
        print(json.dumps(result, indent=2))
        
        if result['success']:
            print("\n✅ Pipeline completed successfully!")
        else:
            print("\n❌ Pipeline failed!")
            sys.exit(1)


if __name__ == "__main__":
    main()

