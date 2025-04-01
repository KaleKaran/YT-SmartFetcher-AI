from youtube_transcript_api import YouTubeTranscriptApi

def extract_transcript(video_id):
    """
    Extract transcript from a YouTube video.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Extracted transcript or error message
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
        full_transcript = ' '.join([entry['text'] for entry in transcript])
        return full_transcript
    except Exception as e:
        return f"Error extracting transcript: {str(e)}" 