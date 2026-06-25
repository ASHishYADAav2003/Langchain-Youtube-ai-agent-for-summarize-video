from langchain_nvidia_ai_endpoints import ChatNVIDIA
from chains.prompts import map_prompt, reduce_prompt
from chains.parser import parser
import os

def get_llm():
    """
    Initialize the NVIDIA NIM Chat Model.
    Ensure NVIDIA_API_KEY is set in the environment.
    """
    # Using Llama 3.3 70B via NVIDIA NIM as a powerful default
    return ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

def summarize_map_reduce(chunks: list[str], progress_callback=None) -> str:
    """
    Executes a map-reduce summarization pipeline using LangChain LCEL.
    
    Args:
        chunks (list[str]): The chunks of the transcript.
        progress_callback (callable, optional): A function to report progress (0.0 to 1.0).
        
    Returns:
        str: The final comprehensive summary.
    """
    llm = get_llm()
    
    # 1. Map Chain: Prompt -> LLM -> String
    map_chain = map_prompt | llm | parser
    
    # 2. Reduce Chain: Prompt -> LLM -> String
    reduce_chain = reduce_prompt | llm | parser
    
    total_chunks = len(chunks)
    mapped_summaries = []
    
    # Map Step: Process each chunk
    for i, chunk in enumerate(chunks):
        # Invoke the map chain for the chunk
        chunk_summary = map_chain.invoke({"text": chunk})
        mapped_summaries.append(chunk_summary)
        
        # Report progress for the map phase (allocating 80% of total progress to map)
        if progress_callback:
            progress_callback((i + 1) / total_chunks * 0.8)
            
    # Combine the chunk summaries
    combined_summaries = "\n\n".join(mapped_summaries)
    
    # Pre-reduce progress update
    if progress_callback:
        progress_callback(0.9)
        
    # Reduce Step: Generate final summary
    final_summary = reduce_chain.invoke({"text": combined_summaries})
    
    # Final progress update
    if progress_callback:
        progress_callback(1.0)
        
    return final_summary
