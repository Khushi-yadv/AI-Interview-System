import json
import os

def load_interview_rounds(company):

    file_path = os.path.join(
        "data",
        "companies",
        company,
        "interview_rounds.json"
    )

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("rounds", [])