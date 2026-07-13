import json
import os

def load_roadmap(career):

    file_path = os.path.join(
        "data",
        "roadmaps",
        f"{career.lower().replace(' ', '_')}.json"
    )

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)