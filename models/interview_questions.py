import pandas as pd
import os


def load_interview_questions(company, role, difficulty):

    file_path = os.path.join(
        "data",
        "companies",
        company,
        "interview_questions.csv"
    )

    if not os.path.exists(file_path):
        return []

    df = pd.read_csv(file_path)

    if difficulty == "All":

        questions = df[
            df["Role"] == role
        ]["Question"].tolist()

    else:

        questions = df[
            (df["Role"] == role) &
            (df["Difficulty"] == difficulty)
    ]["Question"].tolist()

    return questions


def get_ideal_answer(company, question):

    file_path = os.path.join(
        "data",
        "companies",
        company,
        "interview_questions.csv"
    )

    if not os.path.exists(file_path):
        return ""

    df = pd.read_csv(file_path)

    row = df[df["Question"] == question]

    if row.empty:
        return ""

    return row.iloc[0]["Answer"]