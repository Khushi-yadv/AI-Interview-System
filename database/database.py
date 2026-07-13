import sqlite3

conn = sqlite3.connect("interview_history.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS interviews(

id INTEGER PRIMARY KEY AUTOINCREMENT,

user_email TEXT,

company TEXT,

role TEXT,

ats_score INTEGER,

interview_score REAL,

resume_name TEXT

)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT,

email TEXT UNIQUE,

password TEXT

)
""")

conn.commit()


def save_interview(user_email,company, role, ats_score, interview_score, resume_name):

    cursor.execute(
        """
        INSERT INTO interviews
        (user_email,company, role, ats_score, interview_score, resume_name)

        VALUES (?, ?, ?, ?, ?, ?)
        """,

        (
            user_email,
            company,
            role,
            ats_score,
            interview_score,
            resume_name
        )
    )

    conn.commit()

def get_history(user_email):

    cursor.execute(

        """
        SELECT *

        FROM interviews

        WHERE user_email=?
        """,

        (user_email,)
    )

    return cursor.fetchall()

def get_interview_analytics(user_email):

    #conn = sqlite3.connect("interview_history.db")
    #cursor = conn.cursor()

    cursor.execute("""
        SELECT company, ats_score, interview_score
        FROM interviews
        WHERE user_email = ?
        """,
        (user_email,)
        )

    #data = cursor.fetchall()

    #conn.close()

    #return data
    
    return cursor.fetchall()

def signup(name, email, password):

    try:

        cursor.execute(
            """
            INSERT INTO users(name,email,password)

            VALUES(?,?,?)
            """,
            (name, email, password)
        )

        conn.commit()

        return True

    except:

        return False


def login(email, password):

    cursor.execute(

        """
        SELECT * FROM users

        WHERE email=? AND password=?
        """,

        (email, password)

    )

    return cursor.fetchone()