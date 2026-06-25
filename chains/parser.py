from langchain_core.output_parsers import StrOutputParser

# Use LangChain's standard String Output Parser to extract text from the LLM response
parser = StrOutputParser()
