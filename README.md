# Coros - Automatic Podcast Sync

Coros Running Watches don't support streaming services – [only MP3 files](https://support.coros.com/hc/en-us/articles/4406180772244-Playing-Music-from-Your-COROS-Watch). This repository automates downloading and syncing podcast episodes to your watch.

**Simply connect your watch and the latest podcasts will automatically sync – without any manual interaction!**

## Features

- 🎧 **Automatic Downloads** of podcast episodes from RSS feeds
- 📝 **Automatic Metadata** (title & artist) written to MP3 files
- ⚡ **Optimized Performance** through local caching
- 🔄 **Easy Configuration** via `.env` file

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/neidigsi/coros_podcasts.git
cd coros_podcasts
```

### 2. Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Launch Agent

A **LaunchAgent** is a macOS mechanism that automatically runs scripts when your Coros watch is connected. 

For detailed setup instructions, see the [Launch Agent Setup Guide](launchagents/README.md).

## Configuration

### Create .env File

Copy `example.env` as a starting point:

```bash
cp example.env .env
```

### Configure .env

```dotenv
# Target directory for downloaded podcasts
OUTPUT_DIR=/Volumes/PACE 4/Music/auto_sync_podcasts

# Number of episodes per podcast
PODCAST_LIMIT=5

# RSS feeds as JSON array
RSS_FEEDS=["https://feeds.megaphone.fm/vergecast", "https://your-podcast-feed.com/rss"]
```

## Usage

### Simple Execution

```bash
python scripts/main.py
```

The script will then:
1. Read RSS feeds
2. Download new episodes
3. Set MP3 metadata (title & artist)
4. Copy files to the configured directory

## Project Structure

```
coros_podcasts/
├── scripts/
│   ├── main.py          # Main script with orchestration
│   ├── rss.py           # RSS download & metadata processing
├── requirements.txt     # Python dependencies
├── .env                 # Configuration (not versioned)
├── example.env          # Example configuration
├── README.md            # This file
└── LICENSE              # Apache 2.0
```

## Troubleshooting

### Error: "Output directory does not exist"

```bash
# Make sure the directory exists
mkdir -p /path/to/output/dir

# Or use a relative path
OUTPUT_DIR=./podcasts
```

### Error: "No read/write permissions for directory"

```bash
# Check permissions
ls -l /path/to/output/dir

# Adjust permissions
chmod 755 /path/to/output/dir
```

### Error: "RSS_FEEDS must be a valid JSON array"

Make sure `RSS_FEEDS` is a valid JSON array:

```dotenv
# ✅ Correct
RSS_FEEDS=["https://example.com/feed1", "https://example.com/feed2"]

# ❌ Wrong
RSS_FEEDS=https://example.com/feed1
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).

## Contributing

Contributions are welcome! Please create a pull request or open an issue.

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review your `.env` configuration
3. Open an issue with detailed error messages