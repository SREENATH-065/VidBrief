import streamlit as st
from utils.summarizer import summarize_transcript
from utils.embedder import embed_transcript
from utils.qa_engine import get_relevant_context, answer_question
from utils.mcq_generator import generate_mcqs, parse_quiz_questions
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from anthropic import Anthropic

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

st.set_page_config(page_title="VidBrief", layout="wide")
st.title("🎥 VidBrief – AI-Powered YouTube Summarizer & Quiz")

# Initialize session state
for key in ["chat_history", "quiz_answers", "quiz_questions", "quiz_submitted", "vectorstore"]:
    if key not in st.session_state:
        st.session_state[key] = [] if 'quiz' in key or key == 'chat_history' else False

# Extract video ID from YouTube URL
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

# Main UI
yt_url = st.text_input("Enter YouTube URL")

if yt_url and st.button("Analyze Video"):
    video_id = extract_video_id(yt_url)
    if not video_id:
        st.error("❌ Invalid YouTube URL")
    else:
        with st.spinner("Fetching transcript..."):
            try:
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = " ".join([entry['text'].replace('\n', ' ').strip() for entry in transcript_data])
                st.session_state.transcript = transcript
            except Exception as e:
                st.error(f"Transcript fetch failed: {e}")
                st.stop()

        # Punctuate transcript using Claude
        with st.spinner("Punctuating transcript..."):
            prompt = f"""
Please add proper punctuation, capitalization, and paragraph breaks to the following transcript.
Make it readable while preserving the original content and meaning. Don't change any words.

Transcript:
{st.session_state.transcript}
"""
            try:
                response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=4000,
                    temperature=0.2,
                    messages=[{"role": "user", "content": prompt}]
                )
                if isinstance(response.content, list):
                    punctuated = " ".join(
                        block.text.replace("\n", " ") if hasattr(block, "text") else str(block) for block in response.content
                    )
                elif hasattr(response.content, "text"):
                    punctuated = response.content.text.replace("\n", " ")
                else:
                    punctuated = str(response.content).replace("\n", " ")
                st.session_state.punctuated_transcript = punctuated.strip()
            except Exception as e:
                st.error(f"⚠️ Failed to punctuate transcript: {e}")
                st.session_state.punctuated_transcript = st.session_state.transcript

        st.subheader("📝 Punctuated Transcript")
        with st.expander("View Transcript", expanded=False):
            st.text_area("Transcript", st.session_state.punctuated_transcript[:5000] + "..." if len(st.session_state.punctuated_transcript) > 5000 else st.session_state.punctuated_transcript, height=300)

        with st.spinner("Summarizing transcript..."):
            summary = summarize_transcript(client, st.session_state.transcript)
            st.session_state.summary = summary

        st.subheader("📄 Summary")
        st.write(summary)

        with st.spinner("Indexing transcript for Q&A..."):
            st.session_state.vectorstore = embed_transcript(st.session_state.transcript)

# Q&A Section (if transcript was processed)
if st.session_state.get("vectorstore"):
    st.subheader("🧠 Ask Questions")
    user_question = st.text_input("Ask a question about the video")

    if st.button("Ask"):
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

    if st.session_state.chat_history:
        st.subheader("💬 Chat History")
        for i, qa in enumerate(st.session_state.chat_history, 1):
            with st.expander(f"Q{i}: {qa['question']}"):
                st.markdown(f"**Answer:** {qa['answer']}")
                st.caption(f"Confidence: {qa['confidence']:.2f}")

# Quiz Section
st.subheader("📝 Quiz Time")
if st.button("Generate Quiz") and st.session_state.get("transcript"):
    with st.spinner("Generating quiz questions from transcript..."):
        quiz_text = generate_mcqs(st.session_state.transcript, client)
        questions = parse_quiz_questions(quiz_text)
        st.session_state.quiz_questions = questions
        st.session_state.quiz_submitted = False
        st.session_state.quiz_answers = {}  # Reset quiz answers to avoid index errors

if st.session_state.get("quiz_questions"):
    st.write("### Answer the following questions:")
    for i, q in enumerate(st.session_state.quiz_questions, 1):
        st.markdown(f"**Q{i}:** {q['question']}")
        options = [f"{k}) {v}" for k, v in q['options'].items()]
        selected = st.radio("", options, key=f"quiz_{i}")
        if selected:
            st.session_state.quiz_answers[i] = selected[0].lower()
        st.markdown("---")

    if st.button("Submit Quiz"):
        score = 0
        total = len(st.session_state.quiz_questions)
        for i, q in enumerate(st.session_state.quiz_questions, 1):
            if st.session_state.quiz_answers.get(i) == q['correct_answer']:
                score += 1
        st.success(f"🎉 Your Score: {score} / {total} ({(score/total)*100:.1f}%)")

# Footer
st.markdown("---")
st.markdown("Built with 💡 by VidBrief Team")
