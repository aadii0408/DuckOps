# app_alex.py

import streamlit as st
from alex import ResearchAssistantAgent
import os

st.set_page_config(page_title="Alex – Professor & Research Lab Assistant", page_icon="🎓")

def main():
    st.title("🎓 Meet Alex – Your AI Assistant at Stevens")

    # Confirm the app is running
    st.markdown("✅ App is loaded and running...")
    print("✅ Streamlit app started")

    # Check file paths exist
    lab_pdf_path = "stevens_research_network.pdf"
    prof_csv_path = "Professor_Data_2.csv"

    if not os.path.exists(lab_pdf_path) or not os.path.exists(prof_csv_path):
        st.error("❌ Required data files are missing. Make sure both the PDF and CSV are in the same folder.")
        st.stop()

    # Initialize Alex
    if "alex" not in st.session_state:
        st.session_state.alex = ResearchAssistantAgent(prof_csv_path, lab_pdf_path)
        print("✅ Alex loaded")

    # Instruction input
    instruction = st.sidebar.text_area(
        "🧠 Instruction Prompt for Alex",
        value="You are Alex, an AI assistant for answering questions about professors and research labs at Stevens."
    )

    # Question input
    user_question = st.text_input("❓ Ask Alex a question")

    if user_question:
        print(f"📨 Question received: {user_question}")
        response = st.session_state.alex.answer_question(user_question, instruction)
        print(f"📤 Response: {response}")
        st.markdown(f"**🤖 Alex:** {response}")
    else:
        st.info("Ask me anything about professors or labs!")

if __name__ == "__main__":
    main()
