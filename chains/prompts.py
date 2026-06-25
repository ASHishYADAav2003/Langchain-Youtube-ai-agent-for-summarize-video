from langchain_core.prompts import PromptTemplate

# Prompt for the initial map step (summarizing individual chunks)
MAP_PROMPT_TEMPLATE = """
You are an expert content summarizer. 
Please write a concise and informative summary of the following section of a video transcript:

"{text}"

CONCISE SUMMARY:
"""
map_prompt = PromptTemplate.from_template(MAP_PROMPT_TEMPLATE)

# Prompt for the reduce step (combining chunk summaries into a final summary)
REDUCE_PROMPT_TEMPLATE = """
You are an expert content summarizer.
The following is a set of summaries generated from different parts of a video:

"{text}"

Take these summaries and distill them into a final, comprehensive summary of the main points of the entire video.
Provide the final summary in a clear and structured format. Use markdown, headings, and bullet points where appropriate to make it highly readable.

FINAL COMPREHENSIVE SUMMARY:
"""
reduce_prompt = PromptTemplate.from_template(REDUCE_PROMPT_TEMPLATE)
