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

# Input fields
subject = st.text_input("📘 What subject are you teaching?")
grade = st.selectbox("🎓 Grade Level", [f"Grade {i}" for i in range(1, 13)])
pacing = st.radio("⏱️ How fast do you want to move?", ["Slow", "Normal", "Fast"])
selected_days = st.multiselect("🗓️ On which days do you teach this subject?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

# Internal topic mapping database
sample_curricula = {
    ("World History", "Grade 9"): [
        "Origins of Civilization",
        "Ancient Mesopotamia and Egypt",
        "Classical Greece and Rome",
        "Medieval Europe",
        "Islamic Caliphates",
        "Renaissance and Reformation",
        "Age of Exploration",
        "Industrial Revolution",
        "World Wars",
        "Post-Colonial Independence Movements"
    ],
    ("Biology", "Grade 10"): [
        "Scientific Method & Lab Safety",
        "Cell Structure and Function",
        "Genetics",
        "Evolution",
        "Ecology",
        "Human Body Systems"
    ],
    ("English", "Grade 8"): [
        "Short Stories",
        "Poetry and Figurative Language",
        "Drama - Shakespeare",
        "Persuasive Writing",
        "Research Project",
        "Novel Study"
    ],
    ("Navi: Yehoshua", "Grade 9"): [
        "Introduction to Navi & Sefer Yehoshua",
        "Crossing the Jordan",
        "Conquest of Jericho",
        "Achan and the Battle of Ai",
        "The Givonim Deception",
        "Southern Campaign",
        "Northern Campaign",
        "Division of the Land",
        "Cities of Refuge",
        "Final Address of Yehoshua"
    ],
    ("Navi: Shoftim", "Grade 9"): [
        "Overview of the Era of Shoftim",
        "Devorah and Barak",
        "Gideon and the Midianites",
        "Yiftach and His Vow",
        "Shimshon the Judge",
        "Tribe of Dan’s Idolatry",
        "Pilegesh B’Givah and Civil War"
    ],
    ("Navi: Shmuel I", "Grade 9"): [
        "Introduction to Sefer Shmuel",
        "Birth of Shmuel",
        "The Call of Shmuel",
        "Eli and the Ark",
        "Shaul’s Rise as King",
        "War with Amalek",
        "David and Goliath",
        "Shaul’s Jealousy",
        "David’s Fugitive Years",
        "Shaul’s Downfall"
    ],
    ("Navi: Shmuel II", "Grade 10"): [
        "David Becomes King",
        "Conquest of Jerusalem",
        "Uzzah and the Ark",
        "David’s Covenant",
        "Batsheva and Uriah",
        "Nathan’s Rebuke",
        "Amnon and Tamar",
        "Avshalom’s Revolt",
        "Sheva ben Bichri",
        "David’s Final Acts"
    ],
    ("Navi: Melachim I", "Grade 10"): [
        "Coronation of Shlomo",
        "Building the Beit Hamikdash",
        "Shlomo’s Wisdom",
        "Downfall of Shlomo",
        "Division of the Kingdom",
        "Eliyahu HaNavi and the Drought",
        "Har HaCarmel Showdown",
        "Naboth’s Vineyard",
        "Ahaziah and Fire from Heaven"
    ],
    ("Navi: Melachim II", "Grade 10"): [
        "Elisha’s Miracles",
        "Siege of Shomron",
        "Chizkiyahu’s Reforms",
        "Sancheriv’s Invasion",
        "Menashe’s Idolatry",
        "Yoshiyahu’s Torah Discovery",
        "Destruction of the Temple"
    ]
}

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
