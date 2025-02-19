import yt_dlp
import whisper
import os
from moviepy.editor import VideoFileClip

model = whisper.load_model("base")

def download_youtube_video(youtube_url):
    try:
        # Setting options for yt-dlp
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Download best video and audio
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Save file in a folder called 'downloads'
            'quiet': False
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            video_url = info_dict.get('url', None)
            video_file = ydl.prepare_filename(info_dict)
            return video_file
        
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None

def transcribe_video(video_path):
    try:
        # Extract audio
        audio_path = video_path.rsplit(".", 1)[0] + ".mp3"
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, codec="mp3")

        # Transcribe using Whisper
        result = model.transcribe(audio_path)
        transcript = result["text"]

        # Cleanup
        os.remove(audio_path)

        return transcript
    
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
