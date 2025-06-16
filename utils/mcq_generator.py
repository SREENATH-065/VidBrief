import re
from typing import List, Dict, Any


def generate_mcqs(transcript: str, client, num_questions: int = 3) -> str:
    """
    Generate multiple-choice questions from a video transcript.

    Args:
        transcript: The video transcript text
        client: Anthropic client instance
        num_questions: Number of questions to generate (default: 3)

    Returns:
        Generated MCQs as formatted string
    """
    prompt = f"""
Generate {num_questions} multiple-choice questions (MCQs) based on the following video transcript.
Each question should:
- Test comprehension of key concepts from the transcript
- Have 4 options (a-d) with only one correct answer
- Be clear and unambiguous
- Cover different parts of the content

Format each question exactly as follows:

Question X: [Your question here]
a) [Option A]
b) [Option B] 
c) [Option C]
d) [Option D]

Correct Answer: [letter]

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        # Handle different response formats
        if isinstance(response.content, list):
            return "\n".join(
                block.text if hasattr(block, "text") else str(block)
                for block in response.content
            )
        elif hasattr(response.content, "text"):
            return response.content.text
        else:
            return str(response.content)

    except Exception as e:
        print(f"Error generating MCQs: {e}")
        return ""


def parse_quiz_questions(quiz_text: str) -> List[Dict[str, Any]]:
    """
    Parse quiz text into structured question data.

    Args:
        quiz_text: Raw quiz text from MCQ generation

    Returns:
        List of question dictionaries
    """
    questions = []

    # Split by "Question" to get individual questions
    question_blocks = re.split(r'Question \d+:', quiz_text)[1:]  # Skip first empty element

    for block in question_blocks:
        block = block.strip()
        if not block:
            continue

        # Extract question text (everything before first option)
        question_match = re.search(r'^(.*?)(?=\na\))', block, re.DOTALL)
        if not question_match:
            continue

        question_text = question_match.group(1).strip()

        # Extract options
        options = {}
        for letter in ['a', 'b', 'c', 'd']:
            option_pattern = rf'{letter}\)\s*(.*?)(?=\n[a-d]\)|$|\nCorrect Answer:)'
            option_match = re.search(option_pattern, block, re.DOTALL)
            if option_match:
                options[letter] = option_match.group(1).strip()

        # Extract correct answer
        correct_match = re.search(r'Correct Answer:\s*([a-d])', block, re.IGNORECASE)
        correct_answer = correct_match.group(1).lower() if correct_match else None

        if question_text and len(options) == 4 and correct_answer:
            questions.append({
                'question': question_text,
                'options': options,
                'correct_answer': correct_answer
            })

    return questions
