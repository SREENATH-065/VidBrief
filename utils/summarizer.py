def summarize_transcript(client, transcript: str):
    try:
        prompt = f"""
You are a helpful assistant. Summarize the following YouTube video transcript in a concise and clear way:

Transcript:
{transcript}

Summary:
"""
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

    except Exception as e:
        print("Claude API error during summarization:", e)
        return "Summary not available due to an error.".content[0].text.strip()