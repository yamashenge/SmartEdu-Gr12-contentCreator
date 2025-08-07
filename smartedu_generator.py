import streamlit as st
import time
import os
import requests
from dotenv import load_dotenv

# Load Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Page config
st.set_page_config(page_title="SmartEdu - Grade 12 Generator", page_icon="🎓", layout="wide")

# Header
st.markdown("<h1 style='text-align: center;'>📘 SmartEdu: Grade 12 CAPS Content Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate CAPS-aligned content for Grade 12 learners — lesson plans, study guides, quizzes, and more.</p>", unsafe_allow_html=True)
st.markdown("---")

# Input layout
col1, col2 = st.columns(2)

with col1:
    subject = st.selectbox("📚 Subject", ["Mathematics","Physical Science" ,"English", "Life Sciences", "Geography", "History"])

with col2:
    content_type = st.selectbox("📝 Content Type", ["Lesson Plan", "Study Guide", "Quiz Generator", "Revision Summary", "Homework"])

# Fixed grade
grade = "Grade 12"
st.markdown(f"🎓 **Target Grade:** {grade}")

# Topic input
topic = st.text_input("💡 Topic", placeholder="e.g., Organic Chemistry", help="Enter the specific topic you'd like content about.")

# Length slider
length = st.slider("📏 Desired Length (in words)", 100, 1000, 300, step=50)

# API call function
def generate_with_gemini(prompt: str):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(GEMINI_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise Exception(f"{response.status_code} - {response.text}")

# Generate content section
st.markdown("### ✨ AI-Generated Educational Content")

if st.button("🪄 Generate Content"):
    if topic:
        prompt = (
            f"You are a skilled South African teacher creating CAPS-aligned {content_type.lower()} "
            f"for {grade} learners.\n\n"
            f"Subject: {subject}\n"
            f"Topic: {topic}\n"
            f"Length: Approximately {length} words.\n\n"
            f"Please include a clear structure, relevant examples, and assessments or questions where appropriate."
        )

        with st.spinner("🧠 Thinking... Generating content using Gemini AI..."):
            try:
                start = time.time()
                output = generate_with_gemini(prompt)
                duration = round(time.time() - start, 2)

                st.success(f"✅ Content Ready! (Generated in {duration} seconds)")
                st.text_area("📄 Your Educational Content:", output, height=350)
                st.download_button("💾 Download as .txt", output, file_name=f"{subject}_{content_type}_Grade12.txt")

            except Exception as e:
                st.error(f"❌ Error generating content: {e}")
    else:
        st.warning("⚠️ Please enter a topic before generating content.")

# Footer
st.markdown("---")
st.markdown("<small style='color: gray;'>Built with ❤️ using Streamlit and Google Gemini • SmartEdu AI - Grade 12 Edition</small>", unsafe_allow_html=True)
