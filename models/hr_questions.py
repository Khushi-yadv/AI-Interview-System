import json
import os

def load_hr_questions(company):

    company_questions = []
    common_questions = []

    # Company Questions
    company_path = os.path.join(
        "data",
        "companies",
        company.lower(),
        "hr_questions.json"
    )

    if os.path.exists(company_path):

        with open(company_path, "r", encoding="utf-8") as f:

            data = json.load(f)

            company_questions = data.get("questions", [])

    # Common Questions
    common_path = os.path.join(
        "data",
        "hr_questions",
        "common.json"
    )

    if os.path.exists(common_path):

        with open(common_path, "r", encoding="utf-8") as f:

            data = json.load(f)

            common_questions = data.get("questions", [])

    return company_questions, common_questions