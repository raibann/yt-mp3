import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from pathlib import Path

# Spotify API credentials
SPOTIFY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"


def check_spotify_credentials():
    """Check if Spotify credentials are properly configured."""
    if (
        SPOTIFY_CLIENT_ID == "YOUR_SPOTIFY_CLIENT_ID"
        or SPOTIFY_CLIENT_SECRET == "YOUR_SPOTIFY_CLIENT_SECRET"
    ):
        print("❌ Spotify API credentials not configured!")
        print("\nTo use Spotify playlist downloads, you need to:")
        print("1. Go to https://developer.spotify.com/dashboard")
        print("2. Create a new app")
        print("3. Get your Client ID and Client Secret")
        print("4. Update the credentials in spotify.py:")
        print("   SPOTIFY_CLIENT_ID = 'your_actual_client_id'")
        print("   SPOTIFY_CLIENT_SECRET = 'your_actual_client_secret'")
        return False
    return True


# Set download directory
DOWNLOAD_DIR = "/Users/raibann/Documents/projects/github/yt-mp3/spotify_downloaded_mp3"
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)


def get_spotify_playlist_tracks(playlist_url):
    """Get all tracks from a Spotify playlist."""
    # Initialize Spotify client
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Extract playlist ID from URL
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    # Get playlist tracks
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]

    # Handle pagination if there are more tracks
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    # Extract track names and artists
    track_info = []
    for track in tracks:
        if track["track"]:  # Check if track exists
            track_name = track["track"]["name"]
            artist_name = track["track"]["artists"][0]["name"]
            track_info.append(f"{track_name} {artist_name}")

    return track_info


def download_from_youtube(search_query):
    """Download audio from YouTube based on search query."""
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "quiet": False,
        "no_warnings": False,
        "extract_audio": True,
        "audio_format": "mp3",
        "default_search": "ytsearch1:",  # Search on YouTube
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        print(f"Successfully downloaded: {search_query}")
    except Exception as e:
        print(f"Error downloading {search_query}: {str(e)}")


def download_spotify_playlist(playlist_url):
    """Download all tracks from a Spotify playlist."""
    if not check_spotify_credentials():
        return

    print("Fetching tracks from Spotify playlist...")
    tracks = get_spotify_playlist_tracks(playlist_url)

    print(f"Found {len(tracks)} tracks. Starting downloads...")
    for track in tracks:
        print(f"\nSearching for: {track}")
        download_from_youtube(track)

    print("\nAll downloads completed!")


if __name__ == "__main__":
    playlist_url = input("Enter Spotify Playlist URL: ")
    download_spotify_playlist(playlist_url)
