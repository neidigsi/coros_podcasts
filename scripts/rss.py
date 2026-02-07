import os
import feedparser
import requests
import subprocess
import sys
from urllib.parse import urlparse
from mutagen.easyid3 import EasyID3
import time


def send_notification(title: str, message: str) -> None:
    """Send a native macOS notification."""
    try:
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(
            ["osascript", "-e", script],
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Warning: Could not send notification: {e}", file=sys.stderr)


def log_error(message: str) -> None:
    """Log error message and send notification."""
    print(f"Error: {message}")
    send_notification("Podcast Sync - Error", message)


def download_file(url: str, target_path: str) -> float:
    """Download a file from a URL to the given target path. Returns elapsed time."""
    start_time = time.time()
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    elapsed = time.time() - start_time
    return elapsed


def get_filename_from_url(url: str) -> str:
    """Extract filename from URL."""
    return os.path.basename(urlparse(url).path)


def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename."""
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename.strip()


def set_mp3_metadata(file_path: str, title: str, artist: str) -> None:
    """Set ID3 metadata tags on an MP3 file."""
    try:
        audio = EasyID3(file_path)
    except:
        # If file has no ID3 tags, create new ones
        from mutagen.id3 import ID3
        audio = ID3()
    
    if title:
        audio['title'] = title
    if artist:
        audio['artist'] = artist
    
    audio.save(file_path, v2_version=3)


def download_latest_rss_podcasts(feed_url: str, target_dir: str, limit: int) -> None:
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        log_error("No podcast entries found in RSS feed.")
        return

    os.makedirs(target_dir, exist_ok=True)

    entries = feed.entries[:limit]
    total_time = 0
    file_count = 0

    for entry in entries:
        if not entry.enclosures:
            continue

        audio_url = entry.enclosures[0].get("href")
        if not audio_url:
            continue

        title = entry.get('title', 'Unknown title')
        artist = feed.feed.get('title', 'Unknown artist')
        
        # Generate filename as "artist - title"
        original_filename = get_filename_from_url(audio_url)
        file_extension = os.path.splitext(original_filename)[1]
        sanitized_title = sanitize_filename(title)
        sanitized_artist = sanitize_filename(artist)
        filename = f"{sanitized_artist} - {sanitized_title}{file_extension}"
        file_path = os.path.join(target_dir, filename)

        if os.path.exists(file_path):
            print(f"Skipping existing file: {filename}")
            continue

        print(f"Downloading: {title}")
        download_time = download_file(audio_url, file_path)
        
        # Set metadata on MP3
        set_mp3_metadata(file_path, title, artist)
        print(f"Saved to: {file_path}")
        print(f"  Metadata - Title: {title}, Artist: {artist}")
        print(f"  Download time: {download_time:.2f}s")
        
        total_time += download_time
        file_count += 1
    
    if file_count > 0:
        print(f"\n--- Summary ---")
        print(f"Downloaded {file_count} file(s)")
        print(f"Total time: {total_time:.2f}s")
        print(f"Avg time per file: {total_time/file_count:.2f}s")


def download_multpile_rss_podcasts(rss_feeds, output_dir, limit) -> None:
    """Download latest podcasts from multiple RSS feeds."""

    # Download podcasts from each feed
    for feed_url in rss_feeds:
        try:
            print(f"\nProcessing feed: {feed_url}")
            download_latest_rss_podcasts(feed_url, output_dir, limit)
        except Exception as e:
            error_message = f"Error downloading from {feed_url}: {e}"
            log_error(error_message)