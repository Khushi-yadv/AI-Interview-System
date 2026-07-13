import json
import os

RESOURCE_PATH = "data/resources"

def load_resources(role):

    resources = []

    for file in os.listdir(RESOURCE_PATH):

        if file.endswith(".json"):

            with open(
                os.path.join(RESOURCE_PATH, file),
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                if role in data.get("roles", []):
                    resources.append(data)

    return resources