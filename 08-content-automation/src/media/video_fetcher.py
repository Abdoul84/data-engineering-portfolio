"""
Video Fetcher (In-Memory)

Fetches stock footage from Pexels API and streams directly to memory.
No local file storage required.
"""

from io import BytesIO
from typing import Optional, Dict, List
import logging
import requests
import time


logger = logging.getLogger(__name__)


class VideoFetcher:
    """Fetch stock videos from Pexels API with in-memory streaming."""
    
    BASE_URL = "https://api.pexels.com/videos"
    
    def __init__(self, api_key: str):
        """
        Initialize video fetcher.
        
        Args:
            api_key: Pexels API key (free tier: 200 requests/hour)
        """
        if not api_key or api_key == "YOUR_PEXELS_API_KEY":
            raise ValueError("Valid Pexels API key required")
        
        self.api_key = api_key
        self.headers = {"Authorization": api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        logger.info("Video Fetcher initialized with Pexels API")
    
    def search_videos(
        self, 
        query: str, 
        per_page: int = 5,
        orientation: str = "portrait"  # portrait for TikTok/Reels
    ) -> List[Dict]:
        """
        Search for videos on Pexels.
        
        Args:
            query: Search query (e.g., "lion african savanna")
            per_page: Number of results to return (max 80)
            orientation: Video orientation (portrait, landscape, square)
            
        Returns:
            List of video metadata dictionaries
            
        Raises:
            RuntimeError: If API request fails
        """
        try:
            params = {
                "query": query,
                "per_page": min(per_page, 80),
                "orientation": orientation
            }
            
            response = self.session.get(
                f"{self.BASE_URL}/search",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            videos = data.get('videos', [])
            
            logger.info(f"Found {len(videos)} videos for query: '{query}'")
            
            return videos
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to search videos: {e}")
            raise RuntimeError(f"Video search failed: {e}") from e
    
    def get_best_video_url(self, video: Dict, prefer_quality: str = "hd") -> Optional[str]:
        """
        Extract best video file URL from video metadata.
        
        Args:
            video: Video metadata from Pexels API
            prefer_quality: Preferred quality (hd, sd)
            
        Returns:
            Video file URL or None if not found
        """
        video_files = video.get('video_files', [])
        
        if not video_files:
            return None
        
        # Try to find preferred quality with portrait orientation
        for vf in video_files:
            if vf.get('quality') == prefer_quality and vf.get('width', 0) < vf.get('height', 0):
                return vf.get('link')
        
        # Fallback: any portrait video
        for vf in video_files:
            if vf.get('width', 0) < vf.get('height', 0):
                return vf.get('link')
        
        # Last resort: first available video
        return video_files[0].get('link')
    
    def download_video_to_memory(self, url: str, chunk_size: int = 8192) -> BytesIO:
        """
        Download video directly to memory without saving to disk.
        
        Args:
            url: Direct video file URL
            chunk_size: Download chunk size in bytes
            
        Returns:
            BytesIO stream containing video data
            
        Raises:
            RuntimeError: If download fails
        """
        try:
            response = self.session.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            video_stream = BytesIO()
            total_downloaded = 0
            
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    video_stream.write(chunk)
                    total_downloaded += len(chunk)
            
            # Reset stream position
            video_stream.seek(0)
            
            logger.info(f"Downloaded video to memory ({total_downloaded / 1024 / 1024:.2f} MB)")
            
            return video_stream
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download video: {e}")
            raise RuntimeError(f"Video download failed: {e}") from e
    
    def fetch_video(self, animal: str, location: str) -> Optional[BytesIO]:
        """
        Search and fetch a video based on animal and location.
        
        Args:
            animal: Animal name (e.g., "lion")
            location: Location name (e.g., "African savanna")
            
        Returns:
            BytesIO stream with video data, or None if not found
        """
        # Try multiple search strategies
        search_queries = [
            f"{animal} {location}",
            f"{animal} wildlife",
            f"{animal} nature",
            animal
        ]
        
        for query in search_queries:
            try:
                logger.info(f"Searching for: '{query}'")
                videos = self.search_videos(query, per_page=5)
                
                if not videos:
                    continue
                
                # Get first suitable video
                video = videos[0]
                video_url = self.get_best_video_url(video)
                
                if not video_url:
                    continue
                
                # Download to memory
                return self.download_video_to_memory(video_url)
                
            except Exception as e:
                logger.warning(f"Failed with query '{query}': {e}")
                continue
        
        logger.error(f"Could not find video for {animal} / {location}")
        return None
    
    def cleanup(self, video_stream: BytesIO):
        """
        Clean up video stream to free memory.
        
        Args:
            video_stream: BytesIO stream to close
        """
        if video_stream and not video_stream.closed:
            video_stream.close()
            logger.debug("Video stream closed and memory freed")
    
    def close(self):
        """Close the requests session."""
        self.session.close()
        logger.info("Video fetcher session closed")


def main():
    """CLI entry point for testing."""
    import sys
    import os
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🎬 Video Fetcher (In-Memory)\n")
    print("=" * 80)
    
    # Get API key from environment or user
    api_key = os.environ.get('PEXELS_API_KEY')
    
    if not api_key:
        print("⚠️  No PEXELS_API_KEY environment variable found")
        api_key = input("Enter your Pexels API key: ").strip()
    
    if not api_key:
        print("❌ API key required")
        sys.exit(1)
    
    try:
        # Initialize fetcher
        fetcher = VideoFetcher(api_key)
        
        # Test search
        animal = "lion"
        location = "African savanna"
        
        print(f"\n🔍 Searching for: {animal} in {location}")
        
        # Fetch video
        video_stream = fetcher.fetch_video(animal, location)
        
        if video_stream:
            size_mb = len(video_stream.getvalue()) / 1024 / 1024
            print(f"\n✅ Success! Video loaded to memory ({size_mb:.2f} MB)")
            print(f"   Stream position: {video_stream.tell()}")
            print(f"   Stream closed: {video_stream.closed}")
            
            # Optional: Save for testing
            save_test = input("\n💾 Save to /tmp/test_video.mp4 for testing? (y/n): ")
            if save_test.lower() == 'y':
                with open('/tmp/test_video.mp4', 'wb') as f:
                    f.write(video_stream.getvalue())
                print("✅ Saved to /tmp/test_video.mp4")
            
            # Cleanup
            fetcher.cleanup(video_stream)
            print("\n🧹 Memory cleaned up")
        else:
            print("\n❌ Could not fetch video")
        
        fetcher.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

