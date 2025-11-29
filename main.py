import os
import yt_dlp
import pygame
import threading
import time
from pathlib import Path


# Set download directory
DOWNLOAD_DIR = "./mp3"
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

# Global variables for music control
current_song_index = 0
music_files = []
is_playing = False
is_paused = False


# Function to download YouTube playlist as MP3
def download_playlist(playlist_url):
    ydl_opts = {
        # Use more compatible format selection
        "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
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
        "noplaylist": False,
        # Add retry options for fragment issues
        "retries": 10,
        "fragment_retries": 10,
        "skip_unavailable_fragments": True,
        # Add user agent and other headers for better compatibility
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        # Add cookies and other options for YouTube Music (removed problematic browser options)
        # Ignore errors for unavailable videos
        "ignoreerrors": True,
        # Additional options for better YouTube Music compatibility
        "extract_flat": False,
        "writeinfojson": False,
        "writesubtitles": False,
        "writeautomaticsub": False,
        # Add extractor args for better YouTube Music support
        "extractor_args": {
            "youtube": {"player_client": ["android", "web"], "skip": ["dash", "hls"]}
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred during download: {str(e)}")
        print("Trying alternative method...")
        download_playlist_alternative(playlist_url)


# Alternative download method with different settings
def download_playlist_alternative(playlist_url):
    ydl_opts_alt = {
        "format": "worst[ext=m4a]/worst[ext=webm]/worst",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }
        ],
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "quiet": False,
        "no_warnings": False,
        "extract_audio": True,
        "audio_format": "mp3",
        "noplaylist": False,
        "retries": 5,
        "fragment_retries": 5,
        "skip_unavailable_fragments": True,
        "ignoreerrors": True,
        # Additional compatibility options
        "extract_flat": False,
        "writeinfojson": False,
        "extractor_args": {
            "youtube": {"player_client": ["ios", "android"], "skip": ["hls"]}
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_alt) as ydl:
            ydl.download([playlist_url])
        print("Alternative download completed successfully!")
    except Exception as e:
        print(f"Alternative download also failed: {str(e)}")
        print("Please try a different playlist or check your internet connection.")


# Function to load music files
def load_music_files():
    global music_files
    music_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp3")]
    return music_files


# Function to stop music
def stop_music():
    global is_playing, is_paused
    pygame.mixer.music.stop()
    is_playing = False
    is_paused = False
    print("Music stopped.")


# Function to pause/resume music
def pause_music():
    global is_playing, is_paused
    if is_playing and not is_paused:
        pygame.mixer.music.pause()
        is_paused = True
        print("Music paused.")
    elif is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        print("Music resumed.")


# Function to play next song
def next_song():
    global current_song_index, is_playing
    if not music_files:
        print("No music files loaded.")
        return

    current_song_index = (current_song_index + 1) % len(music_files)
    play_current_song()
    print(f"Next song: {music_files[current_song_index]}")


# Function to play previous song
def previous_song():
    global current_song_index, is_playing
    if not music_files:
        print("No music files loaded.")
        return

    current_song_index = (current_song_index - 1) % len(music_files)
    play_current_song()
    print(f"Previous song: {music_files[current_song_index]}")


# Function to play current song
def play_current_song():
    global is_playing, is_paused
    if not music_files:
        print("No music files loaded.")
        return

    file_path = os.path.join(DOWNLOAD_DIR, music_files[current_song_index])
    print(f"Playing: {music_files[current_song_index]}")
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    is_playing = True
    is_paused = False


# Function to handle user input
def handle_input():
    global is_playing
    while is_playing:
        try:
            command = input().strip().lower()

            if command in ["n", "next"]:
                next_song()
            elif command in ["p", "prev"]:
                previous_song()
            elif command in ["s", "stop"]:
                stop_music()
            elif command == "pause":
                pause_music()
            elif command in ["q", "quit"]:
                stop_music()
                print("Goodbye!")
                break
            else:
                print(
                    "Unknown command. Type 'n' for next, 'p' for previous, 's' to stop, 'pause' to pause/resume, or 'q' to quit."
                )
        except EOFError:
            break
        except Exception as e:
            print(f"Input error: {e}")
            break


# Function to play all music files with controls
def play_music():
    global music_files, current_song_index, is_playing

    music_files = load_music_files()
    if not music_files:
        print("No MP3 files found. Download some first!")
        return

    pygame.mixer.init()
    current_song_index = 0

    print("\n=== Music Player Controls ===")
    print("Commands:")
    print("  'n' or 'next' - Next song")
    print("  'p' or 'prev' - Previous song")
    print("  's' or 'stop' - Stop music")
    print("  'pause' - Pause/Resume music")
    print("  'q' or 'quit' - Quit player")
    print("=============================\n")

    # Start playing the first song
    play_current_song()

    # Start input handling in a separate thread
    input_thread = threading.Thread(target=handle_input, daemon=True)
    input_thread.start()

    # Main music monitoring loop
    try:
        while is_playing:
            # Check if music finished playing
            if is_playing and not is_paused and not pygame.mixer.music.get_busy():
                next_song()
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_music()
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error in music player: {e}")
        stop_music()


if __name__ == "__main__":
    playlist_url = input("Enter YouTube Playlist URL: ")
    download_playlist(playlist_url)
    print("\nDownload completed! Playing the files...\n")
    play_music()
