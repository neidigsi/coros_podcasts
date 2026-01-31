import os
import json
import shutil
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from rss import download_multpile_rss_podcasts


def validate_output_directory(directory: str) -> bool:
    """Validate that output directory exists and is writable."""
    path = Path(directory).expanduser().resolve()
    
    if not path.exists():
        print(f"Error: Output directory does not exist: {directory}")
        return False
    
    if not path.is_dir():
        print(f"Error: Output path is not a directory: {directory}")
        return False
    
    if not os.access(path, os.W_OK | os.R_OK):
        print(f"Error: No read/write permissions for directory: {directory}")
        return False
    
    # Test write access by creating a temporary file
    try:
        test_file = path / ".test_write"
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        print(f"Error: Cannot write to directory: {e}")
        return False
    
    return True


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


def copy_mp3_files(source_dir: str, target_dir: str) -> None:
    """Copy all MP3 files from source to target directory."""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    mp3_files = list(source_path.glob("*.mp3"))
    
    if mp3_files:
        print(f"\nCopying {len(mp3_files)} MP3 file(s) to {target_dir}...")
        for mp3_file in mp3_files:
            try:
                target_file = target_path / mp3_file.name
                shutil.copy2(mp3_file, target_file)
                print(f"  Copied: {mp3_file.name}")
            except Exception as e:
                print(f"  Error copying {mp3_file.name}: {e}")


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
    
    # Validate output directory
    if not validate_output_directory(output_dir):
        return
    
    # Delete existing MP3 files
    delete_existing_mp3_files(output_dir)
    
    # Create temporary local directory for downloading
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Download podcasts to local temp directory
        download_multpile_rss_podcasts(rss_feeds, temp_dir, limit)
        
        # Copy MP3 files from temp directory to target volume
        copy_mp3_files(temp_dir, output_dir)
    
    print("\nCompleted!")


if __name__ == "__main__":
    main()
