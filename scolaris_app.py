import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Scolaris AI Curriculum Planner", layout="centered")
st.title("📚 Scolaris: AI Curriculum Generator")

st.markdown("""
Tell us what you're teaching and when — Scolaris will build your curriculum automatically.
""")

# Upload calendar
uploaded_calendar = st.file_uploader("📅 Upload your school calendar (.csv with a 'Date' column)", type=["csv"])

# Internal topic mapping database
sample_curricula = {
    ("World History", "Grade 9"): [...],
    ("Biology", "Grade 10"): [...],
    ("English", "Grade 8"): [...],
    ("Navi: Yehoshua", "Grade 9"): [...],
    ("Navi: Shoftim", "Grade 9"): [...],
    ("Navi: Shmuel I", "Grade 9"): [...],
    ("Navi: Shmuel II", "Grade 10"): [...],
    ("Navi: Melachim I", "Grade 10"): [...],
    ("Navi: Melachim II", "Grade 10"): [...]
}

# Generate dropdown from database
subject_options = sorted(set([key[0] for key in sample_curricula.keys()]))
subject = st.selectbox("📘 What subject are you teaching?", subject_options)
grade = st.selectbox("🎓 Grade Level", sorted(set([key[1] for key in sample_curricula.keys()])))
pacing = st.radio("⏱️ How fast do you want to move?", ["Slow", "Normal", "Fast"])
selected_days = st.multiselect("🗓️ On which days do you teach this subject?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

# Generate lesson plan
if st.button("🚀 Build My Curriculum"):
    if not uploaded_calendar or not subject or not grade or not selected_days:
        st.warning("Please complete all required fields.")
    else:
        calendar_df = pd.read_csv(uploaded_calendar)
        calendar_df['Date'] = pd.to_datetime(calendar_df['Date'])
        calendar_df['Day'] = calendar_df['Date'].dt.day_name()
        teaching_days = calendar_df[calendar_df['Day'].isin(selected_days)].sort_values('Date').reset_index(drop=True)

        # Try to fetch predefined topics
        key = (subject.strip(), grade.strip())
        if key not in sample_curricula:
            st.error(f"No preloaded curriculum found for {subject} ({grade}). Add it to the database.")
        else:
            topics = sample_curricula[key]

            # Adjust pacing
            multiplier = {"Slow": 2, "Normal": 1, "Fast": 0.5}[pacing]
            expanded_topics = []
            for topic in topics:
                repeat = max(1, round(multiplier))
                expanded_topics.extend([topic] * repeat)

            total_days = len(teaching_days)
            lesson_plan = []
            topic_index = 0

            for i, row in teaching_days.iterrows():
                if topic_index < len(expanded_topics):
                    lesson_plan.append({
                        "Date": row['Date'].date(),
                        "Day": row['Day'],
                        "Subject": subject,
                        "Topic": expanded_topics[topic_index]
                    })
                    topic_index += 1
                else:
                    lesson_plan.append({
                        "Date": row['Date'].date(),
                        "Day": row['Day'],
                        "Subject": subject,
                        "Topic": "Review / Flex / Assessment"
                    })

            df = pd.DataFrame(lesson_plan)
            st.success("Curriculum generated successfully!")
            st.dataframe(df)
            st.download_button("📥 Download Curriculum CSV", df.to_csv(index=False).encode(), "curriculum_plan.csv")
