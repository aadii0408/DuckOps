# import os
# import streamlit as st
# from dotenv import load_dotenv
# from langchain.chains import RetrievalQA
# from langchain.chains import ConversationalRetrievalChain
# from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings

# # Load environment variables
# load_dotenv()
# load_dotenv()

# # Verify if the API key is loaded
# api_key = os.getenv("OPENAI_API_KEY")
# if api_key:
#     print("OpenAI API Key is set.")
# else:
#     print("OpenAI API Key is not set. Please check your configuration.")


# # Page configuration
# st.set_page_config(page_title="StevensAI 🦅", page_icon="🦅", layout="wide")

# # Custom CSS for professional UI
# st.markdown(
#     """
#     <style>
#     body {
#         background-color: #F5F5F5;
#         font-family: 'Arial', sans-serif;
#     }
#     .main-title {
#         font-size: 36px;
#         color: #A32638; /* Stevens Red */
#         text-align: center;
#         font-weight: bold;
#         margin-bottom: 20px;
#     }
#     .subtitle {
#         font-size: 18px;
#         color: #333333;
#         text-align: center;
#         margin-bottom: 30px;
#     }
#     .stTextInput>div>div>input {
#         border-radius: 8px;
#         border: 1px solid #A32638;
#         padding: 12px;
#         font-size: 16px;
#     }
#     .stButton>button {
#         background-color: #A32638;
#         color: white;
#         border-radius: 8px;
#         font-size: 16px;
#         padding: 8px 16px;
#         transition: 0.3s;
#     }
#     .stButton>button:hover {
#         background-color: #7B1C2A;
#         transform: scale(1.02);
#     }
#     .chat-container {
#         border-radius: 10px;
#         background-color: white;
#         padding: 20px;
#         box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
#         margin-bottom: 20px;
#         max-height: 400px;
#         overflow-y: auto;
#     }
#     .user-message {
#         background-color: #E6E6E6;
#         padding: 10px 15px;
#         border-radius: 15px 15px 0 15px;
#         margin: 5px 0;
#         max-width: 80%;
#         margin-left: auto;
#         text-align: right;
#     }
#     .bot-message {
#         background-color: #F0F7FF;
#         border-left: 3px solid #A32638;
#         padding: 10px 15px;
#         border-radius: 15px 15px 15px 0;
#         margin: 5px 0;
#         max-width: 80%;
#     }
#     .sender {
#         font-weight: bold;
#         font-size: 14px;
#         margin-bottom: 5px;
#     }
#     .message {
#         font-size: 16px;
#     }
#     .footer {
#         text-align: center;
#         color: #666;
#         font-size: 14px;
#         margin-top: 30px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Initialize session state for chat history if it doesn't exist
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []


# def get_vectorstore():
#     """Initialize or load the vector database"""
#     embeddings = OpenAIEmbeddings()

#     # Check if vector store exists
#     if os.path.exists("faiss_index") and os.path.exists("faiss_index/index.faiss"):
#         # Load existing vector store
#         return FAISS.load_local("faiss_index", embeddings)
#     else:
#         # This should not happen in production - vector store should be created separately
#         st.error(
#             "Vector database not found. Please ensure data ingestion has been completed."
#         )
#         return None


# def get_conversational_chain():
#     """Create a conversational chain with memory and RAG capabilities"""
#     vectorstore = get_vectorstore()
#     if not vectorstore:
#         return None

#     # Initialize language model
#     llm = ChatOpenAI(temperature=0.2)

#     # Create memory object
#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#     # Create prompt template
#     template = """
#     You are StevensAI, a helpful and knowledgeable assistant for Stevens Institute of Technology.
#     Answer questions based on the provided context about Stevens University. Be concise, accurate and helpful.
#     If you don't know the answer based on the provided context, say "I don't have enough information about that" rather than making up an answer.

#     Context: {context}

#     Chat History: {chat_history}

#     Human: {question}
#     AI Assistant:
#     """

#     prompt = PromptTemplate(
#         input_variables=["context", "chat_history", "question"], template=template
#     )

#     # Create retrieval chain
#     chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
#         chain_type_kwargs={"verbose": True, "prompt": prompt, "memory": memory},
#         return_source_documents=True,
#     )

#     return chain


# def process_query(query):
#     """Process user query and get response from LLM"""
#     chain = get_conversational_chain()
#     if not chain:
#         return "I'm having trouble accessing my knowledge base. Please try again later."

#     # Get response from chain
#     response = chain({"query": query})

#     # Add to chat history for display
#     st.session_state.chat_history.append(("You", query))
#     st.session_state.chat_history.append(("StevensAI 🦅", response["result"]))

#     return response["result"]


# # Main interface
# st.markdown('<p class="main-title">StevensAI 🦅</p>', unsafe_allow_html=True)
# st.markdown(
#     '<p class="subtitle">Your intelligent assistant for Stevens Institute of Technology</p>',
#     unsafe_allow_html=True,
# )

# # Chat history display
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)
# for sender, message in st.session_state.chat_history:
#     if sender == "You":
#         st.markdown(
#             f'<div class="user-message"><div class="sender">{sender}</div><div class="message">{message}</div></div>',
#             unsafe_allow_html=True,
#         )
#     else:
#         st.markdown(
#             f'<div class="bot-message"><div class="sender">{sender}</div><div class="message">{message}</div></div>',
#             unsafe_allow_html=True,
#         )
# st.markdown("</div>", unsafe_allow_html=True)

# # Input area
# query = st.text_input(
#     "Ask me anything about Stevens:",
#     placeholder="e.g., What transportation options are available?",
# )

# col1, col2, col3 = st.columns([5, 1, 5])
# with col2:
#     if st.button("Ask 🔍"):
#         if query:
#             with st.spinner("Thinking..."):
#                 response = process_query(query)
#         else:
#             st.warning("Please enter a question!")

# # Footer
# st.markdown(
#     '<div class="footer">Powered by Team DuckOps 🦆 for Stevens students</div>',
#     unsafe_allow_html=True,
# )


# ----------------------------------------------------------------------------------------------------------

# import os
# import streamlit as st
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()


# # Initialize session state for chat history if it doesn't exist
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []


# def process_query(query, use_faiss=True):
#     """Process user query and get response from LLM"""

#     from agent import get_agent  # Ensure we can access the agent class

#     agent = get_agent(use_faiss=use_faiss)  # Choose whether to use FAISS or in-memory

#     response = agent.query(query)

#     # Add to chat history for display
#     st.session_state.chat_history.append(("You", query))
#     st.session_state.chat_history.append(("StevensAI 🦅", response))


# # Main interface setup using Streamlit.
# st.title("Stevens AI Chatbot")
# query_input = st.text_input("Ask me anything about Stevens:")

# if st.button("Ask 🔍"):
#     if query_input:
#         with st.spinner("Thinking..."):
#             process_query(
#                 query_input, use_faiss=True
#             )  # Set to False for in-memory only.

# # Display chat history
# for sender, message in st.session_state.chat_history:
#     st.write(f"**{sender}**: {message}")


# ----------------------------------------------------------------------------------------------------------
import streamlit as st
import os
from dotenv import load_dotenv
from agent import StevensAgent  # Import the StevensAgent class
import ingest  # Import the ingest module

# Load API key
load_dotenv()
st.set_page_config(page_title="Stevens AI Chatbot", page_icon="🎓", layout="wide")

st.title("Stevens AI Chatbot 🤖")
st.subheader("Ask me anything about Stevens Institute!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Function to initialize the agent (or re-initialize if needed)
def initialize_agent():
    if "agent" not in st.session_state or not os.path.exists(
        "faiss_index"
    ):  # Check if the agent exisit if not and there is no faiss_index it will intialize
        print("Initializing or Re-initializing agent...")
        try:
            if not os.path.exists("faiss_index"):
                st.warning(
                    "FAISS index not found. Running data ingestion... This may take a moment."
                )
                ingest.ingest_data()  # Run ingestion if the index doesn't exist
            st.session_state.agent = StevensAgent()
            st.success("Agent initialized successfully!")
        except Exception as e:
            st.error(f"Error initializing agent: {e}")
            st.session_state.agent = None  # Ensure agent is None in case of failure


# Initialize agent on first run or if the index is missing
initialize_agent()


query = st.text_input("🔍 Type your question:")

if st.button("Ask AI"):
    if query:
        if st.session_state.agent is None:
            st.error(
                "Agent is not initialized. Please check the initialization process."
            )
        else:
            response = st.session_state.agent.query(query)

            # Save chat history
            st.session_state.chat_history.append(("🧑‍🎓 You", query))
            st.session_state.chat_history.append(("🤖 StevensBOT", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}**: {message}")

st.markdown("---")

if st.button("Re-ingest Data"):
    st.warning("Re-ingesting data. This will clear the existing vector store.")
    ingest.clear_vector_store()
    initialize_agent()
    st.success("Data re-ingested and agent re-initialized.")
