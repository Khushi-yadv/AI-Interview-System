import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def evaluate_with_ai(question, answer):

    prompt = f"""
You are an expert technical interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer and provide:

1. Score out of 10
2. Strengths
3. Weaknesses
4. Suggested Better Answer
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return (
            "⚠️ AI feedback is temporarily unavailable because the "
            "Gemini API quota has been exceeded. Please try again later."
        )