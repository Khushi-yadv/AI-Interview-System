def evaluate_answer(answer):
    """
    Simple rule-based evaluation.
    Later we will replace this with AI (Gemini/OpenAI).
    """

    if not answer.strip():
        return {
            "score": 0,
            "feedback": "No answer provided."
        }

    words = len(answer.split())

    if words >= 80:
        score = 10
        feedback = "Excellent detailed answer."

    elif words >= 50:
        score = 8
        feedback = "Good answer. Add one or two examples."

    elif words >= 25:
        score = 6
        feedback = "Average answer. Explain concepts in more detail."

    else:
        score = 4
        feedback = "Very short answer. Add explanation and examples."

    return {
        "score": score,
        "feedback": feedback
    }