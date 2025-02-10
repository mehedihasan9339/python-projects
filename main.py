# main.py
from summarizer.ai_text_summarizer import run_app
from transcriber.video_to_text import transcribe_video

if __name__ == '__main__':
    video_file = "test_video.mp4"
    transcript = transcribe_video(video_file)
    print("Transcription:", transcript)

    run_app()  # Run your AI text summarizer
