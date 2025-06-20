# 🎥 VidBrief — AI-Powered YouTube Summarizer, Quiz Generator & Q&A App

**VidBrief** is an AI-powered application that converts YouTube videos into concise summaries, generates interactive MCQ quizzes, and enables semantic Q&A — all from a single video URL. It uses advanced NLP tools like Whisper, Claude, LangChain, and FAISS to break down long videos into digestible and interactive learning elements.

---

## 🌐 Live Demos

### ▶️ Streamlit Web App  
🔗 [Launch VidBrief on Streamlit](https://vidbrief.streamlit.app)

### 📓 Google Colab Notebook  
🔗 [Run in Google Colab](https://colab.research.google.com/drive/1Z3yp73RgaRNJ2cB_fbnsA9WKvyj53ClT)

---

## ✨ Features

- 📄 **AI Summarization** — Generate short, readable summaries of any YouTube video via Claude.
- 🎙️ **Smart Transcription** — Uses Whisper (local) or YouTubeTranscriptAPI (fallback) to get video transcripts.
- ❓ **Semantic Q&A** — Ask natural-language questions and get meaningful answers powered by LangChain + FAISS.
- 📝 **Quiz Generator** — Claude generates multiple-choice questions from the video content.
- 🎮 **(Coming Soon)** Gamified quiz experience for enhanced learning.
- ⚙️ **Dual Deployment** — Works on both Streamlit Cloud and Google Colab.

---

## 🛠 Tech Stack

- `Python`
- `Streamlit` (Frontend UI)
- `Google Colab` (Notebook version)
- `yt-dlp` + `FFmpeg` (Download + audio extraction)
- `Whisper` (Local ASR)
- `YouTubeTranscriptAPI` (Fast transcript fallback)
- `Claude API` (Summary + MCQs)
- `LangChain` (Q&A engine)
- `Hugging Face Transformers` (Embeddings)
- `FAISS` (Semantic similarity search)

---

## 📁 Project Structure

vidbrief/
├── app.py # Streamlit frontend logic
├── utils/
│ ├── downloader.py
│ ├── embedder.py
│ ├── mcq_generator.py
│ ├── qa_engine.py
│ ├── summarizer.py
│ └── transcriber.py
├── requirements.txt
└── README.md


> ⚠️ Note: The Google Colab notebook is not in this repo. It's hosted [here](https://colab.research.google.com/drive/1Z3yp73RgaRNJ2cB_fbnsA9WKvyj53ClT).

---

## ⚙️ Setup Instructions

### ▶️ Run Locally (Streamlit)

```bash
git clone https://github.com/SREENATH-065/VidBrief.git
cd VidBrief
pip install -r requirements.txt
Create a .env file:
CLAUDE_API_KEY=your_claude_api_key

Then launch:

streamlit run app.py

Make sure FFmpeg is installed and accessible via your system PATH.
🧪 Run on Colab
Use this hosted notebook:
🔗 Colab Notebook

🚀 Use Cases
Summarize long YouTube lectures into concise notes

Generate quizzes for test prep or revision

Perform semantic search on spoken content

Enable fast comprehension of tutorials, interviews, etc.
🧭 Roadmap
 Streamlit App

 Claude-based summarization + quiz

 Whisper + transcript fallback

 LangChain Q&A

 Gamified quiz (in development)

 Topic-based summarization

 Voice-based question answering

📜 License
MIT License © 2025 SREENATH S
