import streamlit as st
from utils.summarizer import summarize_transcript
from utils.embedder import embed_transcript
from utils.qa_engine import get_relevant_context, answer_question
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from anthropic import Anthropic

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

st.set_page_config(page_title="VidBrief", layout="wide")
st.title("🎥 VidBrief – AI-Powered YouTube Summarizer (Deployable Version)")

# Extract video ID
def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    elif parsed.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query).get('v', [None])[0]
        elif parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
        elif parsed.path.startswith('/v/'):
            return parsed.path.split('/')[2]
    return None

yt_url = st.text_input("Enter YouTube URL")

if yt_url and st.button("Summarize"):
    video_id = extract_video_id(yt_url)
    if not video_id:
        st.error("❌ Invalid YouTube URL")
    else:
        with st.spinner("Fetching transcript..."):
            try:
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = " ".join([entry['text'] for entry in transcript_data])
                st.session_state.transcript = transcript
            except Exception as e:
                st.error(f"Transcript fetch failed: {e}")
                st.stop()


        # 🔽 Summarization
        with st.spinner("Summarizing..."):
            summary = summarize_transcript(client, st.session_state.transcript)
            st.session_state.summary = summary

        st.subheader("📄 Summary")
        st.write(summary)

        with st.spinner("Indexing transcript for Q&A..."):
            st.session_state.vectorstore = embed_transcript(st.session_state.transcript)

# Chat history init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Q&A UI
user_question = st.text_input("Ask a question about the video", key="qa_input")

if st.button("Ask"):
    if user_question.lower().strip() in ["quit", "exit", "q"]:
        st.success("🎉 Thanks for using VidBrief!")
        st.session_state.chat_history = []
        st.stop()

    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Getting answer from Claude..."):
            context = get_relevant_context(st.session_state.vectorstore, user_question)
            result = answer_question(client, user_question, context)

            st.session_state.chat_history.append({
                'question': user_question,
                'answer': result['answer'],
                'confidence': result['confidence']
            })

# Display Q&A history
if st.session_state.chat_history:
    st.subheader("🧠 Chat History")
    for i, qa in enumerate(st.session_state.chat_history, 1):
        st.markdown(f"**Q{i}:** {qa['question']}")
        st.markdown(f"**A{i}:** {qa['answer']}")
        st.caption(f"Confidence: {qa['confidence']:.2f}")
        st.markdown("---")

# Footer
st.markdown("💡 Type `quit` to end the conversation.")
