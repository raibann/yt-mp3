# YouTube MP3 Downloader

A Python application that downloads audio from YouTube playlists and Spotify playlists, converting them to MP3 format for offline listening.

## Features

- **YouTube Playlist Download**: Download entire YouTube playlists as MP3 files
- **Spotify Playlist Download**: Download tracks from Spotify playlists by searching YouTube
- **Audio Playback**: Built-in music player using pygame
- **High Quality Audio**: Downloads audio in 192kbps MP3 format
- **Easy to Use**: Simple command-line interface

## Requirements

- Python 3.11.11 or higher
- uv (Python package manager)
- FFmpeg (for audio conversion)
- Spotify API credentials (for Spotify playlist downloads)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd yt-mp3
```

2. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies using uv:
```bash
uv sync
```

4. Install FFmpeg:
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Usage

### YouTube Playlist Download

Run the main script to download a YouTube playlist:

```bash
uv run python main.py
```

Enter the YouTube playlist URL when prompted. The script will:
1. Download all videos from the playlist as MP3 files
2. Save them to the `downloaded_mp3/` directory
3. Automatically play the downloaded music

### Spotify Playlist Download

For Spotify playlists, you'll need to set up Spotify API credentials first:

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app and get your Client ID and Client Secret
3. Update the credentials in `spotify.py`:
   ```python
   SPOTIFY_CLIENT_ID = "your_client_id_here"
   SPOTIFY_CLIENT_SECRET = "your_client_secret_here"
   ```

Then run:
```bash
uv run python spotify.py
```

Enter the Spotify playlist URL when prompted. The script will:
1. Fetch track information from the Spotify playlist
2. Search for each track on YouTube
3. Download the best matching audio as MP3
4. Save them to the `spotify_downloaded_mp3/` directory

## Project Structure

```
yt-mp3/
├── main.py                 # YouTube playlist downloader
├── spotify.py             # Spotify playlist downloader
├── downloaded_mp3/        # YouTube downloads directory
├── spotify_downloaded_mp3/ # Spotify downloads directory
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## Dependencies

- `yt-dlp`: YouTube video/audio downloading
- `spotipy`: Spotify Web API client
- `pygame`: Audio playback
- `ffmpeg-python`: Audio format conversion

## Notes

- Downloaded files are saved in MP3 format with 192kbps quality
- The application respects YouTube's terms of service
- Make sure you have the right to download the content you're accessing
- Large playlists may take considerable time to download

## License

This project is for educational purposes only. Please respect copyright laws and terms of service of the platforms you're downloading from.
