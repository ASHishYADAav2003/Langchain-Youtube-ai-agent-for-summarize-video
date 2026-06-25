# 🎬 YouTube AI Summarizer Agent

An intelligent AI-powered agent that automatically fetches, processes, and summarizes YouTube videos using LangChain and Large Language Models. Supports long-form videos through smart transcript chunking and multi-stage summarization chains.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Project Architecture](#-project-architecture)
- [File & Module Reference](#-file--module-reference)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Environment Variables](#-environment-variables)
- [Requirements](#-requirements)
- [License](#-license)

---

## 🌐 Live Demo

> 🚀 **Try it live here:** [**youtube-ai-summarizer.streamlit.app**](https://your-app-name.streamlit.app)

No setup required — just open the link, paste a YouTube URL, and get your summary instantly.

> ⚠️ The live demo uses a shared API key with rate limits. For heavy usage, clone the repo and run it locally with your own key.

---

## 🧠 Overview

**YouTube AI Summarizer** is an end-to-end AI agent built with Python that takes a YouTube video URL as input and returns a clean, structured, and detailed summary — without you having to watch the entire video.

It leverages the YouTube Transcript API to fetch subtitles, applies text preprocessing and smart chunking for long videos, and uses LangChain-powered summarization chains backed by an LLM (such as OpenAI GPT or similar) to generate high-quality summaries.

---

## ✨ Features

- 🔗 **URL-based Input** — Just paste a YouTube link and get a summary
- 📄 **Auto Transcript Extraction** — Fetches captions/transcripts directly from YouTube
- 🧹 **Smart Text Cleaning** — Removes noise, timestamps, and irrelevant artifacts
- ✂️ **Long Video Support** — Automatically splits long transcripts into chunks
- 🔗 **Multi-Stage Summarization** — Uses map-reduce style chaining for accuracy
- 📊 **Structured Output** — Returns parsed, formatted summaries ready to read
- 🎨 **Custom UI** — Clean and styled Streamlit web interface
- ⚙️ **Modular Design** — Clean separation of concerns across utils and chains

---

## 📁 Project Architecture

```
youtube-ai-summarizer/
│
├── app.py                  # Main Streamlit application entry point
├── .env                    # Environment variables (API keys, config)
├── requirements.txt        # Python dependencies
│
├── utils/
│   ├── transcript.py       # YouTube transcript fetching
│   ├── cleaner.py          # Raw transcript text cleaning
│   ├── prompts.py          # LLM prompt templates
│   ├── parser.py           # LLM output parsing & formatting
│   ├── splitter.py         # Text chunking for long transcripts
│   ├── llm.py              # LLM client initialization & config
│   └── helper.py           # Shared utility/helper functions
│
├── chains/
│   ├── summary_chain.py    # Per-chunk summarization chain
│   ├── merge_chain.py      # Merges chunk summaries into one
│   └── output_chain.py     # Final output formatting chain
│
├── assets/
│   └── style.css           # Custom CSS styling for the UI
│
└── README.md               # Project documentation
```

---

## 📂 File & Module Reference

### `app.py` — Application Entry Point

The main file that runs the Streamlit web application. It handles:
- UI layout and rendering
- User input (YouTube URL)
- Orchestrating the full summarization pipeline
- Displaying the final summary output to the user

---

### `utils/` — Utility Modules

#### `transcript.py`
Handles fetching the transcript/captions from a given YouTube video URL.
- Extracts the video ID from the URL
- Uses `youtube-transcript-api` to pull available subtitles
- Returns raw transcript text for further processing

#### `cleaner.py`
Preprocesses the raw transcript text before it hits the LLM.
- Removes timestamps and metadata artifacts
- Strips filler words, repeated phrases, and formatting noise
- Normalizes whitespace and punctuation
- Returns a clean, readable version of the transcript

#### `prompts.py`
Defines all the LangChain `PromptTemplate` objects used across chains.
- Chunk-level summarization prompt
- Merge/consolidation prompt
- Final structured output prompt
- Keeps all prompts centralized and easy to tweak

#### `parser.py`
Parses and post-processes LLM output into structured formats.
- Extracts key sections (e.g. main summary, key points, topics)
- Handles formatting inconsistencies in model responses
- Returns clean Python dicts or formatted strings

#### `splitter.py`
Handles intelligent splitting of long transcripts into manageable chunks.
- Uses LangChain's `RecursiveCharacterTextSplitter` or similar
- Configures chunk size and overlap for coherent context windows
- Ensures no critical information is lost at chunk boundaries

#### `llm.py`
Initializes and configures the LLM client used throughout the app.
- Loads model name and API key from environment variables
- Sets parameters like `temperature`, `max_tokens`, etc.
- Returns a reusable LLM instance for all chains

#### `helper.py`
Contains shared utility functions used across the project.
- URL validation and video ID extraction
- Token counting helpers
- Logging utilities
- Any other general-purpose functions

---

### `chains/` — LangChain Summarization Chains

#### `summary_chain.py`
The first-stage chain that summarizes individual transcript chunks.
- Takes a single chunk of cleaned transcript text
- Applies the chunk-level summarization prompt
- Returns a concise summary for that chunk
- Designed to run in parallel/map-reduce fashion

#### `merge_chain.py`
The second-stage chain that merges all chunk-level summaries.
- Takes a list of chunk summaries as input
- Combines them into a single coherent narrative
- Handles deduplication and logical flow between sections
- Core of the map-reduce summarization strategy

#### `output_chain.py`
The final-stage chain that formats the merged summary into structured output.
- Applies the final output prompt
- Produces a clean, readable, and organized summary
- May include sections like: Overview, Key Points, Topics Covered, Conclusion

---

### `assets/style.css` — Custom Styling

Custom CSS injected into the Streamlit UI to improve visual appearance.
- Custom fonts, colors, and layout tweaks
- Styled summary output cards
- Responsive design adjustments

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **Streamlit** | Web application UI framework |
| **LangChain** | LLM chaining & orchestration |
| **OpenAI / Groq / Ollama** | LLM backend for summarization |
| **youtube-transcript-api** | Fetching YouTube transcripts |
| **python-dotenv** | Environment variable management |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/youtube-ai-summarizer.git
cd youtube-ai-summarizer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Now edit .env and add your API keys (see Configuration section)
```

---

## 🔧 Configuration

Create a `.env` file in the root directory with the following variables:

```env
# LLM Provider API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model name override
MODEL_NAME=gpt-4o-mini

# Optional: LLM parameters
TEMPERATURE=0.3
MAX_TOKENS=1000

# Optional: Chunk configuration
CHUNK_SIZE=3000
CHUNK_OVERLAP=200
```

> **Note:** If using Groq or another provider, replace `OPENAI_API_KEY` with the appropriate key and update `utils/llm.py` accordingly.

---

## 🚀 Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

Then open your browser and go to: `http://localhost:8501`

### Steps to Use

1. Paste a valid YouTube video URL into the input field
2. Click the **"Summarize"** button
3. Wait while the agent fetches the transcript and processes it
4. Read the structured summary output on screen

---

## 🔄 How It Works

The summarization pipeline follows a **Map → Reduce → Format** pattern:

```
YouTube URL
     │
     ▼
[transcript.py] ──► Fetch raw transcript from YouTube
     │
     ▼
[cleaner.py] ──────► Clean & normalize the transcript text
     │
     ▼
[splitter.py] ─────► Split into overlapping chunks (for long videos)
     │
     ▼
[summary_chain.py] ─► Summarize each chunk individually  (MAP)
     │
     ▼
[merge_chain.py] ───► Merge all chunk summaries into one (REDUCE)
     │
     ▼
[output_chain.py] ──► Format into structured, readable output (FORMAT)
     │
     ▼
[parser.py] ────────► Parse & extract key sections
     │
     ▼
  Final Summary displayed in Streamlit UI
```

For **short videos** (transcript fits in one context window), the chunking and merge steps are skipped and the summary is generated in a single LLM call.

---

## 📦 Requirements

Key dependencies from `requirements.txt`:

```
streamlit
langchain
langchain-openai          # or langchain-groq / langchain-ollama
youtube-transcript-api
python-dotenv
tiktoken
openai
```

Install all at once with:

```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built with ❤️ by **[Your Name]**

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-profile)

---

> ⭐ If you found this project useful, give it a star on GitHub!
