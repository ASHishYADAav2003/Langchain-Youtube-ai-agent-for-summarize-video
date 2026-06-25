from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str, chunk_size: int = 4000, chunk_overlap: int = 400) -> list[str]:
    """
    Splits a large text into smaller, manageable chunks for the LLM using RecursiveCharacterTextSplitter.
    
    Args:
        text (str): The text to split.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The overlap between chunks to maintain context.
        
    Returns:
        list[str]: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks
