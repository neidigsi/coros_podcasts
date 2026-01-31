import os
import json
from pathlib import Path
from dotenv import load_dotenv
from rss import download_latest_rss_podcasts


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
    
    # Download podcasts from each feed
    for feed_url in rss_feeds:
        try:
            print(f"\nProcessing feed: {feed_url}")
            download_latest_rss_podcasts(feed_url, output_dir, limit)
        except Exception as e:
            print(f"Error downloading from {feed_url}: {e}")


if __name__ == "__main__":
    main()
