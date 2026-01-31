import os
import feedparser
import requests
from urllib.parse import urlparse


def download_file(url: str, target_path: str) -> None:
    """Download a file from a URL to the given target path."""
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def get_filename_from_url(url: str) -> str:
    """Extract filename from URL."""
    return os.path.basename(urlparse(url).path)


def download_latest_rss_podcasts(feed_url: str, target_dir: str, limit: int) -> None:
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        raise RuntimeError("No podcast entries found in RSS feed.")

    os.makedirs(target_dir, exist_ok=True)

    entries = feed.entries[:limit]

    for entry in entries:
        if not entry.enclosures:
            continue

        audio_url = entry.enclosures[0].get("href")
        if not audio_url:
            continue

        filename = get_filename_from_url(audio_url)
        file_path = os.path.join(target_dir, filename)

        if os.path.exists(file_path):
            print(f"Skipping existing file: {filename}")
            continue

        print(f"Downloading: {entry.get('title', 'Unknown title')}")
        download_file(audio_url, file_path)
        print(f"Saved to: {file_path}")