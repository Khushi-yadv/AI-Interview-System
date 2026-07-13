import json
import os

def load_company_description(company):

    file_path = os.path.join(
        "data",
        "companies",
        company,
        "company_info.json"
    )

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)