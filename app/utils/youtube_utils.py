import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_thumbnail(video_id: str) -> str:
    """Get the YouTube thumbnail URL for the given video ID."""
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_transcript(url):
    try:
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
        print(f"Fetching transcript for Video ID: {video_id}")
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join(entry['text'] for entry in transcript_list)
        print(f"Transcript fetched successfully for Video ID: {video_id}")
        return full_transcript
        
    except Exception as e:
        return f"Error: {str(e)}"