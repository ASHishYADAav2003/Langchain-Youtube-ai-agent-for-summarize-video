import re

def clean_text(text: str) -> str:
    """
    Cleans the extracted transcript text to improve LLM processing and export quality.
    
    Args:
        text (str): Raw transcript text.
        
    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
        
    # Replace newlines with spaces to create a continuous flow
    text = text.replace('\n', ' ')
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespaces
    return text.strip()
