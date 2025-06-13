from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_transcript_chunks(transcript: str, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = splitter.create_documents([transcript])
    return docs

def embed_transcript(transcript: str, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    embedding_model = HuggingFaceEmbeddings(model_name=model_name)
    docs = load_transcript_chunks(transcript)
    vectorstore = FAISS.from_documents(docs, embedding_model)
    return vectorstore
