import logging
import google.generativeai as genai
import yt_dlp
import whisper
import os

# Function to download audio from YouTube using yt_dlp
def download_youtube_audio(video_url, output_path="audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.mp4',  # Temporary audio file
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Convert MP4 to MP3 using FFmpeg
    os.system(f"ffmpeg -i audio.mp4 -vn -ar 44100 -ac 2 -b:a 192k {output_path}")

    # Remove the original MP4 file
    os.remove('audio.mp4')

    return output_path

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result['text']

def generate_title_and_summary(text):
    # Configure logging to suppress gRPC logs
    logging.getLogger('absl').setLevel(logging.ERROR)  # Suppress absl logs
    logging.getLogger('grpc').setLevel(logging.ERROR)  # Suppress grpc logs

    # Configure your API key
    genai.configure(api_key="AIzaSyBwNDnAvOMcc0PyE57xeqw1YQ68I0hZrPo")

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use the correct model name
        # Generate title
        title_response = model.generate_content(f"Generate a concise title for this content without bold fonts: {text}")
        title = title_response.text.strip()

        # Generate summary
        summary_response = model.generate_content(f"Summarize this text: {text}")
        summary = summary_response.text.strip()

        return title, summary
    except Exception as e:
        print(f"Error during API request: {str(e)}")
        return "Error generating title", "Error generating summary"

def main(video_url):
    print("Downloading audio...")
    audio_path = download_youtube_audio(video_url)

    print("Transcribing audio...")
    transcript = transcribe_audio(audio_path)

    print("Generating title and summary...")
    title, summary = generate_title_and_summary(transcript)

    print("\nTitle:\n", title)
    print("\nSummary:\n", summary)

    # Cleanup
    os.remove(audio_path)

    return title, summary
