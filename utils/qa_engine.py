from langchain_core.vectorstores import VectorStore

def get_relevant_context(vectorstore: VectorStore, query: str, k=4):
    matched_docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in matched_docs])


def answer_question(client, question: str, context: str):
    try:
        prompt = f"""
You are a helpful assistant. Based on the following transcript, answer the user's question concisely and accurately.

Transcript:
{context}

Question:
{question}

Answer:
"""
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=256,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            'answer': response.content[0].text.strip(),
            'confidence': 1.0
        }

    except Exception as e:
        print("Claude API error:", e)
        return {'answer': "Sorry, couldn't get a response.", 'confidence': 0}
