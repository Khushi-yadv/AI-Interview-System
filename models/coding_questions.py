import json
import os

BASE_PATH = "data/coding_questions"


def load_coding_questions(company, role):

    questions = []

    for file in os.listdir(BASE_PATH):

        if file.endswith(".json"):

            path = os.path.join(BASE_PATH, file)

            with open(path, "r", encoding="utf-8") as f:

                data = json.load(f)

                for question in data:

                    if (
                        company in question["companies"]
                        and role in question["roles"]
                    ):
                        questions.append(question)

    return questions