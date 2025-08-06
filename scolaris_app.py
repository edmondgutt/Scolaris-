import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="Scolaris AI Curriculum Planner", layout="wide")

# ---------- Branding ----------
st.markdown("""
<style>
.big-title {
    font-size: 3em;
    font-weight: bold;
    background: linear-gradient(to right, #2F80ED, #56CCF2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5em;
}
.card {
    background-color: white;
    padding: 2em;
    border-radius: 1em;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    margin-bottom: 1em;
}
.lesson-box {
    background-color: #f7f9fc;
    border-left: 6px solid #2F80ED;
    padding: 1em;
    border-radius: 0.5em;
    margin-bottom: 1em;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📚 Scolaris</div>', unsafe_allow_html=True)
st.markdown("Welcome to your AI-powered curriculum assistant. Upload your school calendar and build your school year in seconds.")

# ---------- Upload Section ----------
st.markdown("---")
st.markdown("### 🔼 Upload Your Calendar")
uploaded_calendar = st.file_uploader("Upload CSV with a 'Date' column", type=["csv"])

# ---------- Form Inputs ----------
st.markdown("---")
st.markdown("### 🧠 Course Information")
with st.form("course_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        subject = st.selectbox("📘 Subject", ["Navi: Shmuel I"])
    with col2:
        grade = st.selectbox("🎓 Grade", ["Grade 9"])
    with col3:
        pacing = st.radio("⏱️ Pacing", ["Slow", "Normal", "Fast"])

    selected_days = st.multiselect("🗓️ Teaching Days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], default=["Tuesday", "Thursday"])
    submitted = st.form_submit_button("🚀 Build My Curriculum")

# ---------- Curriculum Generation Logic ----------
sample_curricula = {
    ("Navi: Shmuel I", "Grade 9"): [
        "Review of Sefer Shoftim",
        "Perek 1 (Pasukim 1–11): Chana's Tefillah",
        "Perek 1 (Pasukim 12–28): Birth of Shmuel",
        "Perek 2: Corruption of Bnei Eli",
        "Perek 3: Shmuel’s First Nevuah",
        "Perek 4: War & Capture of Aron",
        "Perek 5–6: Plishtim & Return of the Aron",
        "Perek 7: Teshuvah and Peace",
        "Perek 8: Request for a King",
        "Perek 9–10: Shaul is Anointed",
        "Perek 11: Shaul’s First Victory",
        "Perek 12: Shmuel’s Farewell Speech",
        "Perek 13–15: Shaul’s Mistakes",
        "Perek 16: David Anointed",
        "Perek 17: David vs. Goliath",
        "Perek 18–19: Shaul’s Jealousy",
        "Perek 20: David and Yonatan",
        "Perek 21–22: David on the Run",
        "Perek 23–24: David Spares Shaul",
        "Perek 25: Naval & Avigayil",
        "Perek 26–27: David Hides",
        "Perek 28: Ba’alat Ov",
        "Perek 29–31: Death of Shaul"
    ]
}

status_file = "curriculum_status.json"
if os.path.exists(status_file):
    with open(status_file, 'r') as f:
        curriculum_status = json.load(f)
else:
    curriculum_status = {}

if submitted:
    if not uploaded_calendar or not subject or not grade or not selected_days:
        st.warning("Please complete all fields and upload your calendar.")
    else:
        calendar_df = pd.read_csv(uploaded_calendar)
        calendar_df['Date'] = pd.to_datetime(calendar_df['Date'])
        calendar_df['Day'] = calendar_df['Date'].dt.day_name()
        teaching_days = calendar_df[calendar_df['Day'].isin(selected_days)].sort_values('Date').reset_index(drop=True)

        key = (subject.strip(), grade.strip())
        topics = sample_curricula.get(key, [])

        multiplier = {"Slow": 3, "Normal": 2, "Fast": 1}[pacing]
        expanded_topics = []
        for topic in topics:
            expanded_topics.extend([topic] * multiplier)

        lesson_plan = []
        for i, row in teaching_days.iterrows():
            if i < len(expanded_topics):
                topic = expanded_topics[i]
            else:
                topic = "Review / Flex / Assessment"

            lesson_plan.append({
                "Date": row['Date'].date().isoformat(),
                "Day": row['Day'],
                "Topic": topic,
                "Activity": "",
                "Homework": "",
                "Notes": "",
                "Status": "Upcoming"
            })

        curriculum_status[subject] = lesson_plan
        with open(status_file, 'w') as f:
            json.dump(curriculum_status, f)
        st.success("Curriculum generated!")

# ---------- Portal View ----------
st.markdown("---")
st.markdown("### 🧑‍🏫 Teacher Portal")
if subject in curriculum_status:
    for i, row in enumerate(curriculum_status[subject]):
        with st.expander(f"📅 {row['Date']} ({row['Day']}): {row['Topic']}"):
            st.markdown("<div class='lesson-box'>", unsafe_allow_html=True)
            activity = st.text_input(f"Class Activity (Row {i})", value=row.get("Activity", ""), key=f"activity_{i}")
            homework = st.text_input(f"Homework (Row {i})", value=row.get("Homework", ""), key=f"homework_{i}")
            notes = st.text_area(f"Notes (Row {i})", value=row.get("Notes", ""), key=f"notes_{i}")

            curriculum_status[subject][i]["Activity"] = activity
            curriculum_status[subject][i]["Homework"] = homework
            curriculum_status[subject][i]["Notes"] = notes

            if st.button(f"✅ Mark as Taught (Row {i})"):
                curriculum_status[subject][i]["Status"] = "Completed"
            if st.button(f"❌ Skip (Row {i})"):
                curriculum_status[subject][i]["Status"] = "Missed"

            st.markdown("</div>", unsafe_allow_html=True)

    with open(status_file, 'w') as f:
        json.dump(curriculum_status, f)
