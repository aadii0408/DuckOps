import streamlit as st
import os
from dotenv import load_dotenv
from agent import StevensAgent
import ingest

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Stevens AI Agent", page_icon="🦆", layout="wide")
st.title("🦆 Meet Duck – Your AI Agent for Stevens")
st.subheader("Ask me anything about Stevens Institute!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Initialize or reinitialize the chatbot
def initialize_agent():
    if "agent" not in st.session_state or not os.path.exists("faiss_index"):
        try:
            if not os.path.exists("faiss_index"):
                st.warning(
                    "FAISS index not found. Running data ingestion... This may take a moment."
                )
                ingest.ingest_data()
            st.session_state.agent = StevensAgent()
            st.success("Agent initialized successfully!")
        except Exception as e:
            st.error(f"Error initializing agent: {e}")
            st.session_state.agent = None


initialize_agent()

# Display chat history
st.markdown("### Chat History")
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}**: {message}")

st.markdown("---")


# Ask question callback
def ask_question():
    user_input = st.session_state["user_input"]
    if user_input and st.session_state.agent:
        response = st.session_state.agent.get_response(user_input)
        st.session_state.chat_history.append(("🦆 Student", user_input))
        st.session_state.chat_history.append(("🤖 Duck", response))
        st.session_state["user_input"] = ""
    elif not st.session_state.agent:
        st.error("Agent is not initialized. Try re-ingesting data.")


# Input and ask button
st.text_input("Type your question:", key="user_input")
st.button("Ask", on_click=ask_question)

st.markdown("---")

# # Re-ingest Data button
# if st.button("Re-ingest Data"):
#     st.warning("Re-ingesting data. This will clear the existing vector store.")
#     ingest.clear_vector_store()
#     initialize_agent()
#     st.session_state.chat_history = []
#     st.write("Chat history cleared. You can start a new conversation.")
