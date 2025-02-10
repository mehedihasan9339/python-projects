import whisper
import os
from moviepy.editor import VideoFileClip

model = whisper.load_model("base")

def transcribe_video(video_path):
    audio_path = video_path.rsplit(".", 1)[0] + ".mp3"
    
    # Extract audio
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec="mp3")

    # Transcribe using Whisper
    result = model.transcribe(audio_path)
    transcript = result["text"]

    # Cleanup
    os.remove(audio_path)

    return transcript
