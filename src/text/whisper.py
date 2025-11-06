"""
YouTube audio download and transcription functionality
Transcription is performed using OpenAI Whisper API
"""

from pathlib import Path
import yt_dlp
from openai import OpenAI


def download_youtube_audio(video_id, output_dir):
    """Download audio from YouTube video and return file path"""
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    output_path = Path(output_dir) / f"{video_id}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": str(Path(output_dir) / f"{video_id}.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return output_path
    except Exception as e:
        raise Exception(f"Failed to download audio: {str(e)}")


def transcribe_audio(audio_path, api_key):
    """Transcribe audio file using OpenAI Whisper API"""
    client = OpenAI(api_key=api_key)

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment", "word"],
        )

    return transcription
