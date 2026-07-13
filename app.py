import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from utils.file_handler import save_uploaded_file
from utils.job_loader import load_job_description
from utils.certificate import generate_certificate

from models.resume_parser import extract_text
from models.skill_extractor import extract_skills
from models.ats_score import calculate_ats_score
from models.recommendations import get_recommendations
from models.interview_questions import load_interview_questions
from models.coding_questions import load_coding_questions
from models.interview_session import get_random_questions
from models.interview_questions import  get_ideal_answer
from models.answer_evaluator import evaluate_answer
from models.ai_evaluator import evaluate_with_ai
from models.pdf_report import generate_report
from models.hr_questions import load_hr_questions
from models.company_description import load_company_description
from models.interview_rounds import load_interview_rounds
from models.roadmap import load_roadmap
from models.resources import load_resources

from data.company_list import COMPANIES
from data.roles import ROLES

from database.database import (
    save_interview,
    get_history,
    get_interview_analytics,
    signup,
    login
)

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Interview Preparation System",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------

st.title("🤖 AI Interview Preparation & Resume Analysis System")

if "user" in st.session_state:

    menu = st.sidebar.selectbox(

        "Account",

        ["Home", "Logout"]

    )

else:

    menu = st.sidebar.selectbox(

        "Account",

        ["Login", "Signup"]

    )


if menu == "Signup":

    st.header("Create Account")

    name = st.text_input("Name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Signup"):

        if signup(name, email, password):

            st.success("Account Created Successfully!")

        else:

            st.error("Email already exists!")

    st.stop()



if menu == "Login":

    st.header("Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login(email, password)

        if user:

            st.session_state["user"] = user

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Email or Password")

    if "user" not in st.session_state:

        st.stop()
        
if menu == "Logout":

    del st.session_state["user"]

    st.success("Logged Out Successfully!")

    st.rerun()

st.divider()

st.header("👋 Welcome!")

st.write("""
This project helps users to:

📄 Analyze Resume

🎯 Match Resume with Job Description

📊 Calculate ATS Score

📈 Find Skill Gaps

🏢 View Company Information

🛣️ Explore Career Roadmaps

📚 Get Personalized Learning Resources

📋 Understand Interview Rounds

❓ Practice Previous Interview Questions

💻 Solve Company Coding Questions

💼 Prepare HR Interview Questions

🤖 Generate AI Interview Questions

📝 Evaluate Interview Answers
""")

st.success("Project Setup Completed Successfully! 🚀")

st.divider()

# -----------------------------
# Resume Upload
# -----------------------------

st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your Resume",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    # Save Resume

    saved_path = save_uploaded_file(uploaded_file)

    st.success("Resume uploaded successfully!")

    st.info(f"Resume saved successfully at:\n{saved_path}")

    # File Details

    st.write("### File Details")

    st.write(f"**File Name:** {uploaded_file.name}")
    st.write(f"**File Type:** {uploaded_file.type}")
    st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

    st.divider()
    st.subheader("👤 Candidate Details")

    candidate_name = st.text_input(
        "Enter Your Name",
        placeholder="Enter your full name"
    )

    # -----------------------------
    # Company & Role
    # -----------------------------

    st.header("🏢 Company & Role Selection")

    selected_company = st.selectbox(
        "Select Company",
        COMPANIES
    )

    selected_role = st.selectbox(
        "Select Role",
        ROLES
    )
    
    difficulty = st.selectbox(

        "🎯 Select Interview Difficulty",

         ["All", "Easy", "Medium", "Hard"]
    )

    # -----------------------------
    # Resume Text
    # -----------------------------

    resume_text = extract_text(saved_path)

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=250
    )

    # -----------------------------
    # Skills
    # -----------------------------

    skills = extract_skills(resume_text)

    st.subheader("🛠️ Extracted Skills")

    if skills:
        for skill in skills:
            st.success(skill)
    else:
        st.warning("No skills found.")

    st.divider()

    # -----------------------------
    # Job Description Source
    # -----------------------------

    mode = st.radio(
        "Choose Job Description Source",
        [
            "Company Database",
            "Paste Job Description"
        ]
    )

    job_description = ""

    if mode == "Company Database":

        if (
            selected_company != "Select Company"
            and selected_role != "Select Role"
        ):

            job_description = load_job_description(
                selected_company,
                selected_role
            )

            if job_description:

                st.subheader("📄 Loaded Job Description")

                st.text_area(
                    "Job Description",
                    job_description,
                    height=250
                )

            else:
                st.warning("Job Description not found.")

        else:
            st.info("Please select Company and Role.")

    elif mode == "Paste Job Description":

        job_description = st.text_area(
            "Paste Job Description Here",
            height=250
        )

    # -----------------------------
    # ATS Score
    # -----------------------------

    if job_description:

        score, matched, missing = calculate_ats_score(
            resume_text,
            job_description
        )

        st.divider()

        st.subheader("📊 ATS Score")

        st.progress(score / 100)

        st.success(f"ATS Score : {score}%")

        st.subheader("✅ Matching Skills")

        if matched:
            for skill in matched:
                st.success(skill)
        else:
            st.warning("No Matching Skills Found.")

        st.subheader("❌ Missing Skills")

        if missing:
            for skill in missing:
                st.error(skill)
        else:
            st.success("No Missing Skills.")

        st.subheader("📚 Learning Recommendations")

        recommendations = get_recommendations(missing)

        if recommendations:

            for skill, suggestion in recommendations:
                st.info(f"**{skill}**\n\n{suggestion}")

        else:
            st.success("Your Resume matches all required skills.")

    st.divider()

    st.subheader("🏢 Company Information")

    company_info = load_company_description(
        selected_company
    )

    if company_info:

        st.write(f"**Company:** {company_info['company']}")
        st.write(f"**Parent Company:** {company_info['parent_company']}")
        st.write(f"**Founded:** {company_info['founded']}")
        st.write(f"**CEO:** {company_info['ceo']}")
        st.write(f"**Headquarters:** {company_info['headquarters']}")
        st.write(f"**Industry:** {company_info['industry']}")
        st.write(f"**Employees:** {company_info['employees']}")

        st.markdown("##### 🚀 Products")
        st.write(", ".join(company_info["products"]))

        st.markdown("##### 💻 Tech Stack")
        st.write(", ".join(company_info["tech_stack"]))

        st.markdown("##### 📋 Interview Process")

        for step in company_info["interview_process"]:
            st.write(f"• {step}")

        st.markdown("##### 💰 Salary")

        st.write(f"Intern : {company_info['salary']['intern']}")
        st.write(f"SDE-1 : {company_info['salary']['sde1']}")
        st.write(f"SDE-2 : {company_info['salary']['sde2']}")

        st.info(company_info["description"])

    else:

        st.warning("Company information not found.")
        
    st.divider()

    st.subheader("🛣️ Career Roadmap")

    roadmap = load_roadmap(selected_role)

    if roadmap:

         st.info(roadmap["description"])

         for step in roadmap["steps"]:

             with st.expander(
                  f"Step {step['step']} • {step['title']}"
             ):

                  for topic in step["topics"]:
                      st.write(f"• {topic}")

    else:

         st.warning("Roadmap not found.")
         
    st.divider()

    st.subheader("📚 Learning Resources")

    resources = load_resources(selected_role)

    for resource in resources:

        with st.expander(f"📘 {resource['skill']}"):

             st.markdown("### 📖 Books")

             for book in resource["books"]:
                 st.write(f"• {book}")

             st.markdown("### 🎓 Courses")

             for course in resource["courses"]:
                 st.write(
                     f"• {course['name']} ({course['platform']})"
                 )

             st.markdown("### ▶️ YouTube")

             for yt in resource["youtube"]:
                 st.write(f"• {yt['channel']}")

             st.markdown("### 💻 Practice Websites")

             for site in resource["practice_websites"]:
                 st.write(f"• {site}")
         
    st.divider()

    st.subheader("📋 Interview Rounds")

    rounds = load_interview_rounds(
        selected_company
    )

    if rounds:

        for item in rounds:

            with st.expander(
                f"Round {item['round']} • {item['name']}"
            ):

                st.write("### Focus Areas")

                for topic in item["focus"]:
                    st.write(f"• {topic}")

    else:

        st.warning("Interview Rounds not found.")
        
    st.divider()

    st.subheader("❓ Previous Interview Questions")

    questions = load_interview_questions(
        selected_company,
        selected_role,
        difficulty
    )
    
    if questions:
        for i, question in enumerate(questions, start=1):
            st.write(f"**{i}. {question}**")
    else:
        st.warning("No Interview Questions Found.")
        
    st.divider()

    st.subheader("💻 Coding Questions")

    coding_questions = load_coding_questions(
        selected_company,
        selected_role
    )
    if difficulty != "All":
      coding_questions = [
        q for q in coding_questions
        if q["difficulty"] == difficulty
    ]

    if coding_questions:

        for i, question in enumerate(coding_questions, start=1):

           with st.expander(f"{i}. {question['title']} ({question['difficulty']})"):

              st.write(f"**Difficulty:** {question['difficulty']}")

              st.write(f"**Tags:** {', '.join(question['tags'])}")

              if question["leetcode"]:
                st.markdown(f"🔗 [LeetCode Problem]({question['leetcode']})")

    else:

        st.warning("No Coding Questions Found for this Company and Role.")
        
    st.divider()
    

    st.subheader("💼 HR Interview Questions")
    
    #st.write("Company:", selected_company)
    #st.write("Role:", selected_role)

    company_questions, common_questions = load_hr_questions(
        selected_company
    )

    st.markdown("##### 🏢 Company Specific HR Questions")

    if company_questions:

        for i, question in enumerate(company_questions, start=1):

             with st.expander(
                  f"{i}. {question['question']}"
             ):

                  st.write(f"**Category:** {question['category']}")
                  st.write(f"**Difficulty:** {question['difficulty']}")
                  st.success(question["answer"])

    else:
        st.warning("No Company HR Questions Found.")


    st.markdown("##### 🌍 Common HR Questions")

    if common_questions:

        for i, question in enumerate(common_questions, start=1):

            with st.expander(
                 f"{i}. {question['question']}"
            ):

                 st.write(f"**Category:** {question['category']}")
                 st.write(f"**Difficulty:** {question['difficulty']}")
                 st.success(question["answer"])
    else:

        st.warning("No HR Questions Found.")
        
    st.divider()
    
    st.subheader("🎤 Mock Interview")

if st.button("Start Mock Interview"):

    interview_questions = get_random_questions(
        questions,
        min(5, len(questions))
    )

    st.session_state["questions"] = interview_questions
    st.session_state["current_question"] = 0
    st.session_state["answers"] = {}

    st.rerun()
    
if "questions" in st.session_state:

    current = st.session_state["current_question"]
    questions = st.session_state["questions"]
    
    if len(questions) == 0:
        st.warning("No interview questions available.")
        st.stop()

    if current >= len(questions):
        st.session_state["current_question"] = 0
        current = 0

    st.subheader(
        f"Question {current + 1} of {len(questions)}"
    )

    st.info(questions[current])

    answer = st.text_area(
        "Your Answer",
        key=current
    )
    
    if "answers" not in st.session_state:
       st.session_state["answers"] = {}

    st.session_state["answers"][current] = answer

    col1, col2 = st.columns(2)
    
    with col1:

      if st.button("⬅️ Previous"):

        if current > 0:

            st.session_state["current_question"] -= 1

            st.rerun()

    with col2:

      if st.button("Next ➡️"):

        if current < len(questions) - 1:

            st.session_state["current_question"] += 1

            st.rerun()
            
            
    if current == len(questions) - 1:

      if st.button("✅ Submit Interview"):

        st.success("Interview Submitted Successfully!")

        st.balloons()

        st.write("### Your Answers")
        
        total_score = 0

        for i, q in enumerate(questions):

            st.markdown(f"**Q{i+1}. {q}**")

            ans = st.session_state["answers"].get(i, "No Answer")

            st.write(ans)
            result = evaluate_answer(ans)
            
            total_score += result["score"]

            st.write(f"⭐ Score: {result['score']}/10")

            st.info(result["feedback"])
            
            st.subheader("🤖 AI Feedback")

            ai_feedback = evaluate_with_ai(q, ans)

            st.write(ai_feedback)
            
            ideal_answer = get_ideal_answer(
               selected_company,
               q
            )

            st.subheader("📖 Ideal Answer")

            st.success(ideal_answer)
            
            st.divider()
            
        overall_score = total_score / len(questions)

        st.header("📊 Overall Interview Report")

        st.metric(
            "Overall Score",
            f"{overall_score:.1f}/10"
        )

        if overall_score >= 8:
           st.success("Excellent Performance! 🎉")

        elif overall_score >= 6:
           st.info("Good Performance. Keep Practicing 👍")

        else:
           st.warning("Needs Improvement. Practice More 💪")
           
        pdf_file = generate_certificate(
             candidate_name,
             selected_company,
             selected_role,
             score,
             overall_score
        )

        with open(pdf_file, "rb") as file:

             st.download_button(
                  "📥 Download Certificate",
                  data=file,
                  file_name="AI_Interview_Certificate.pdf",
                  mime="application/pdf"
             )
           
        pdf_file = generate_report(
            questions,
            st.session_state["answers"],
            overall_score
        )

        with open(pdf_file, "rb") as file:

           st.download_button(
              "📄 Download Interview Report",
              file,
              file_name="Interview_Report.pdf",
              mime="application/pdf"
            )
           
        save_interview(
            st.session_state["user"][2],
            selected_company,
            selected_role,
            score,
            overall_score,
            uploaded_file.name
        )

        st.success("Interview saved successfully!")
        
        st.divider()

        st.header("📚 Interview History")

        history = get_history( st.session_state["user"][2])

        if history:

            for row in history:

                st.write(
                    f"🏢 {row[2]} | "
                    f"💼 {row[3]} | "
                    f"ATS: {row[4]}% | "
                    f"Interview: {row[5]:.1f}/10"
                )

        else:

            st.info("No interview history found.")
            
        st.divider()

        st.header("📈 Performance Dashboard")

# -------- Metrics --------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("ATS Score", f"{score}%")

        with col2:
             st.metric("Interview Score", f"{overall_score:.1f}/10")

        with col3:
              st.metric("Matched Skills", len(matched))

        with col4:
              st.metric("Missing Skills", len(missing))

# -------- Pie Chart --------

        fig, ax = plt.subplots(figsize=(3,3))

        labels = ["Matched", "Missing"]

        sizes = [len(matched), len(missing)]

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontsize": 8}
        )

        ax.set_title("Skill Match Analysis", fontsize=10)

        st.pyplot(fig, use_container_width=False)
        
        st.divider()

        st.header("📈 Interview Trends")

        data = get_interview_analytics(st.session_state["user"][2])

        if data:

            companies = [row[0] for row in data]
            ats_scores = [row[1] for row in data]
            interview_scores = [row[2] for row in data]

            fig2, ax2 = plt.subplots(figsize=(4,2.5))

            ax2.plot(companies, interview_scores, marker="o")

            ax2.set_title("Interview Score Trend")
            ax2.set_xlabel("Company")
            ax2.set_ylabel("Score")

            st.pyplot(fig2, use_container_width=False)

            st.subheader("📊 Statistics")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Total Interviews", len(data))
                st.metric("Highest ATS", f"{max(ats_scores)}%")

            with col2:
                avg = sum(interview_scores) / len(interview_scores)
                st.metric("Average Score", f"{avg:.1f}/10")

                best_company = companies[interview_scores.index(max(interview_scores))]
                st.metric("Best Company", best_company)
                
        else:

            st.info("No interview data available.")
            
        if history:

            df = pd.DataFrame(
                history,
                columns=[
                    "ID",
                    "User Email",
                    "Company",
                    "Role",
                    "ATS Score",
                    "Interview Score",
                    "Resume Name"
                ]
            )

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Interview History (CSV)",
                data=csv,
                file_name="interview_history.csv",
                mime="text/csv"
            )