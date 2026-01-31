import os
import json
from pathlib import Path
from dotenv import load_dotenv
from rss import download_multpile_rss_podcasts


def delete_existing_mp3_files(directory: str) -> None:
    """Delete all MP3 files in the given directory."""
    if not os.path.exists(directory):
        return
    
    mp3_files = list(Path(directory).glob("*.mp3"))
    if mp3_files:
        print(f"Deleting {len(mp3_files)} existing MP3 file(s)...")
        for mp3_file in mp3_files:
            try:
                mp3_file.unlink()
                print(f"  Deleted: {mp3_file.name}")
            except Exception as e:
                print(f"  Error deleting {mp3_file.name}: {e}")
    else:
        print("No existing MP3 files found.")


def main():
    # Load environment variables from .env file
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
    # Get output directory and limit from environment
    output_dir = os.getenv("OUTPUT_DIR", "downloads")
    limit = int(os.getenv("PODCAST_LIMIT", "5"))
    
    # Parse RSS feeds from JSON array
    rss_feeds_json = os.getenv("RSS_FEEDS", "[]")
    try:
        rss_feeds = json.loads(rss_feeds_json)
    except json.JSONDecodeError:
        print("Error: RSS_FEEDS must be a valid JSON array")
        return
    
    if not rss_feeds:
        print("No RSS feed URLs found in .env file")
        return
    
    print(f"Found {len(rss_feeds)} RSS feeds to process")
    print(f"Output directory: {output_dir}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Delete existing MP3 files
    delete_existing_mp3_files(output_dir)
    
    # Download podcasts from RSS feeds
    download_multpile_rss_podcasts(rss_feeds, output_dir, limit)


if __name__ == "__main__":
    main()
