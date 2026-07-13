import os


def load_job_description(company, role):

    role = role.lower().replace(" ", "_")

    filename = f"{role}.txt"

    file_path = os.path.join(
        "data",
        "companies",
        company,
        filename
    )

    if os.path.exists(file_path):

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    return None