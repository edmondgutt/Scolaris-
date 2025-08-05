import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Scolaris Lesson Plan Generator", layout="centered")
st.title("🧠 Scolaris: AI Lesson Plan Generator")

st.markdown("""
Upload your school calendar and fill in your course info.
Scolaris will build your day-by-day lesson plan based on real teaching days.
""")

# Upload school calendar
uploaded_calendar = st.file_uploader("📅 Upload your school calendar (.csv with a 'Date' column)", type=["csv"])

# Subject and grade info
subject = st.text_input("📘 Subject Name (e.g., Math, Biology, History)")
grade = st.selectbox("🎓 Grade Level", [f"Grade {i}" for i in range(1, 13)])

# Weekly schedule selection
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
selected_days = st.multiselect("🗓️ On which days do you teach this subject?", days_of_week)

# Topics to cover
topics_input = st.text_area("📚 List the topics or units you want to cover (one per line)")
topics = [line.strip() for line in topics_input.strip().split("\n") if line.strip()] if topics_input else []

# Generate button
if st.button("🚀 Generate Lesson Plan"):
    if not uploaded_calendar or not subject or not selected_days or not topics:
        st.warning("Please complete all required fields.")
    else:
        # Load calendar
        calendar_df = pd.read_csv(uploaded_calendar)
        calendar_df['Date'] = pd.to_datetime(calendar_df['Date'])

        # Filter only selected days
        calendar_df['Day'] = calendar_df['Date'].dt.day_name()
        teaching_days = calendar_df[calendar_df['Day'].isin(selected_days)].sort_values('Date').reset_index(drop=True)

        # Spread topics across available days
        total_days = len(teaching_days)
        total_topics = len(topics)
        repeat_rate = max(1, total_days // total_topics)

        lesson_plan = []
        topic_index = 0

        for i, row in teaching_days.iterrows():
            if topic_index < total_topics:
                lesson_plan.append({
                    "Date": row['Date'].date(),
                    "Day": row['Day'],
                    "Subject": subject,
                    "Topic": topics[topic_index]
                })
                if (i + 1) % repeat_rate == 0 and topic_index + 1 < total_topics:
                    topic_index += 1
            else:
                lesson_plan.append({
                    "Date": row['Date'].date(),
                    "Day": row['Day'],
                    "Subject": subject,
                    "Topic": "Extension / Review / Assessment"
                })

        result_df = pd.DataFrame(lesson_plan)

        # Show preview
        st.success("Lesson plan generated successfully!")
        st.dataframe(result_df)

        # Download CSV
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Lesson Plan as CSV", data=csv, file_name="lesson_plan.csv", mime="text/csv")
