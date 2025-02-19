from summarizer.ai_text_summarizer import run_app
from transcriber.video_to_text import download_youtube_video, transcribe_video

if __name__ == '__main__':
    youtube_url = "https://www.youtube.com/watch?v=3AIoHLr8nTI"
    video_file = download_youtube_video(youtube_url)
    
    if video_file:
        print(f"Downloaded video: {video_file}")
        transcript = transcribe_video(video_file)
        
        if transcript:
            print("Transcription:", transcript)
            run_app(transcript)  # Run the AI summarizer with the transcription
        else:
            print("Transcription failed.")
    else:
        print("Video download failed.")
