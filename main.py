# from summarizer.ai_text_summarizer import run_app
# from transcriber.video_to_text import download_youtube_video, transcribe_video

# if __name__ == '__main__':
#     youtube_url = "https://www.youtube.com/watch?v=3AIoHLr8nTI"
#     video_file = download_youtube_video(youtube_url)
    
#     if video_file:
#         print(f"Downloaded video: {video_file}")
#         transcript = transcribe_video(video_file)
        
#         if transcript:
#             print("Transcription:", transcript)
#             run_app(transcript)  # Run the AI summarizer with the transcription
#         else:
#             print("Transcription failed.")
#     else:
#         print("Video download failed.")








#   TEXT SUMMARIZER
#   ===============
#   This script uses the Hugging Face Transformers library to summarize text using the BART model.
#   It takes a text input, summarizes it, and then prints the summary.
#   You can also use this script to summarize text from a file or from a YouTube video transcription
from text.text_summarizer import summarize_text

if __name__ == "__main__":
    long_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. 
    Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize 
    its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) 
    that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem-solving".
    """

    print("\n--- Original Text ---\n")
    print(long_text)

    summary = summarize_text(long_text)

    print("\n--- Summarized Text ---\n")
    print(summary)


