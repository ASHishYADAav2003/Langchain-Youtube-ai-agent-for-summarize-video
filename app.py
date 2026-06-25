import streamlit as st
import os
from dotenv import load_dotenv

# Import our utility functions
from utils.helper import extract_video_id
from utils.transcript import get_transcript
from utils.cleaner import clean_text
from utils.splitter import split_text
from utils.exporter import export_to_pdf, export_to_md

# Import our LCEL map-reduce chain
from chains.summary_chain import summarize_map_reduce

# Load environment variables (e.g., NVIDIA_API_KEY)
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="YouTube AI Summarizer",
    page_icon="🎥",
    layout="wide"
)

# Load Custom CSS for UI/UX improvements (Theme compatibility)
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# App Header
st.title("🎥 YouTube AI Summarizer")
st.markdown("Professional-grade YouTube summarization powered by **NVIDIA NIM**, **LangChain LCEL**, and **Streamlit**.")

# Sidebar Instructions
with st.sidebar:
    st.header("📖 How to use")
    st.markdown("""
    1. **Find a Video**: Go to YouTube and copy the URL of the video you want to summarize.
    2. **Paste the URL**: Paste the link into the input box on the main page.
    3. **Generate**: Click the **Generate Summary** button.
    4. **Wait**: The AI will fetch the transcript, chunk it, and generate a comprehensive summary using a Map-Reduce pipeline.
    5. **Export**: Copy the summary or download it as a TXT, Markdown, or PDF file!
    """)
    st.markdown("---")
    st.info("💡 **Note:** The video must have subtitles (either auto-generated or manual) for the AI to summarize it.")

# Main Interface
url = st.text_input("🔗 Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

# Initialize session state for holding the generated summary across reruns
if 'summary' not in st.session_state:
    st.session_state.summary = None

# Summarize Button
if st.button("Generate Summary", type="primary"):
    if not url:
        st.warning("Please enter a valid YouTube URL.")
    elif not os.environ.get("NVIDIA_API_KEY"):
        st.error("Please provide your NVIDIA API Key via the .env file.")
    else:
        video_id = extract_video_id(url)
        
        if not video_id:
            st.error("Invalid YouTube URL. Could not extract the video ID.")
        else:
            try:
                # 1. Fetch Transcript
                with st.spinner("📥 Fetching video transcript..."):
                    raw_transcript = get_transcript(video_id)
                
                # 2. Clean Transcript
                cleaned_text = clean_text(raw_transcript)
                
                # 3. Split Text
                with st.spinner("✂️ Chunking text for processing..."):
                    chunks = split_text(cleaned_text)
                    st.info(f"Video transcript split into {len(chunks)} manageable chunks.")
                
                # 4. Summarize via Map-Reduce
                progress_bar = st.progress(0.0)
                status_text = st.empty()
                status_text.markdown("🤖 **Generating summary (Map-Reduce)...**")
                
                def update_progress(p):
                    progress_bar.progress(p)
                    
                # Run the chain
                final_summary = summarize_map_reduce(chunks, progress_callback=update_progress)
                
                # Clean up status indicators
                status_text.markdown("✅ **Summarization complete!**")
                
                # Save to session state
                st.session_state.summary = final_summary
                
            except Exception as e:
                error_message = str(e)
                if "Failed to fetch transcript" in error_message or "Subtitles are disabled" in error_message:
                    st.warning("🚫 **No Transcript Available:** This video does not have subtitles or any transcript available. The AI needs subtitles to generate a summary. Please try another video that has closed captions (CC).")
                else:
                    st.error(f"An error occurred during processing:\n\n{error_message}")

# Display the summary and export options
if st.session_state.summary:
    st.markdown("---")
    st.markdown("## 📝 Final Summary")
    
    # Render markdown beautifully
    st.markdown(st.session_state.summary)
    
    st.markdown("### 📋 Copy / Raw Markdown")
    with st.expander("Show Raw Markdown (Click to copy)"):
        # st.code provides a native copy button on hover
        st.code(st.session_state.summary, language="markdown")
        
    st.markdown("---")
    st.markdown("## 💾 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    # Download TXT
    with col1:
        st.download_button(
            label="📄 Download TXT",
            data=st.session_state.summary,
            file_name="summary.txt",
            mime="text/plain"
        )
        
    # Download Markdown
    with col2:
        md_content = export_to_md(st.session_state.summary)
        st.download_button(
            label="📝 Download Markdown",
            data=md_content,
            file_name="summary.md",
            mime="text/markdown"
        )
        
    # Download PDF
    with col3:
        try:
            pdf_bytes = export_to_pdf(st.session_state.summary)
            st.download_button(
                label="📕 Download PDF",
                data=pdf_bytes,
                file_name="summary.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error("Failed to generate PDF. Check for special characters in the summary.")
