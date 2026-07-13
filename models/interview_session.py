import random


def get_random_questions(questions, num_questions=5):
    """
    Randomly select interview questions.
    """

    if len(questions) <= num_questions:
        return questions

    return random.sample(questions, num_questions)