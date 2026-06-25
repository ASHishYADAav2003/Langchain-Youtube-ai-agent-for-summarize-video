import re
import urllib.parse

def extract_video_id(url: str) -> str | None:
    """
    Extracts the YouTube video ID from various forms of YouTube URLs.
    
    Args:
        url (str): The YouTube URL.
        
    Returns:
        str | None: The 11-character video ID, or None if not found.
    """
    # Parse URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Handle youtu.be/<id>
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
        
    # Handle youtube.com/watch?v=<id> or youtube.com/shorts/<id>
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        if parsed_url.path == "/watch":
            query = urllib.parse.parse_qs(parsed_url.query)
            return query.get("v", [None])[0]
        elif parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]
            
    return None
