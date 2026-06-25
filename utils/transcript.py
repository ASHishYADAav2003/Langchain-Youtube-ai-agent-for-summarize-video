from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcript(video_id: str) -> str:
    """
    Fetches the transcript for a given YouTube video ID.
    
    Args:
        video_id (str): The 11-character YouTube video ID.
        
    Returns:
        str: The raw text of the transcript.
        
    Raises:
        Exception: If transcript cannot be fetched (e.g., no subtitles, disabled).
    """
    try:
        # Initialize the API client
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch the transcript list for the video
        transcript_list = ytt_api.list(video_id)
        
        # Try to find an English transcript (manual or generated)
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        except Exception:
            # Fallback to the first available transcript (e.g. Hindi, Spanish, etc.)
            first_lang_code = [t.language_code for t in transcript_list][0]
            transcript = transcript_list.find_transcript([first_lang_code])
            
            # Optionally try to translate, but if it fails, just use the original language
            try:
                if getattr(transcript, 'is_translatable', False):
                    transcript = transcript.translate('en')
            except Exception:
                pass # The LLM will receive the original language and translate/summarize it natively

        # Fetch the actual transcript data
        transcript_data = transcript.fetch()
        
        # Format transcript into a single string
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript_data)
        
        return text_formatted
    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}. The video might not have English subtitles or subtitles are disabled.")
