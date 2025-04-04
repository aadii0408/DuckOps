# import os
# from dotenv import load_dotenv
# from langchain.agents import Tool, AgentExecutor, create_react_agent
# from langchain_openai import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
# from langchain_community.vectorstores import FAISS
# from langchain.embeddings.openai import OpenAIEmbeddings
# from pydantic import BaseModel, GetJsonSchemaHandler, validator
# from pydantic_core import CoreSchema
# from typing import Any, Dict

# # Load environment variablesss
# load_dotenv()


# class Config(BaseModel):
#     api_key: str

#     @validator("api_key", allow_reuse=True)
#     def validate_api_key(cls, value):
#         if not value:
#             raise ValueError("API key cannot be empty.")
#         return value

#     @classmethod
#     def __get_pydantic_json_schema__(
#         cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
#     ) -> Dict[str, Any]:
#         json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
#         json_schema = handler.resolve_ref_schema(json_schema)
#         json_schema.update(examples=["example_api_key"])
#         return json_schema


# # Verify if the API key is loaded
# config = Config(api_key=os.getenv("OPENAI_API_KEY"))
# if config.api_key:
#     print("OpenAI API Key is set.")
# else:
#     print("OpenAI API Key is not set. Please check your configuration.")


# class SimpleStevensAgent:
#     def __init__(self, api_key: str, use_faiss=True):
#         self.api_key = api_key  # Set API key directly
#         self.llm = ChatOpenAI(temperature=0.2)
#         self.tools = self._create_tools()
#         self.memory = ConversationBufferMemory(
#             memory_key="chat_history", return_messages=True
#         )
#         self.vectorstore = self._get_vectorstore(use_faiss)
#         self.agent_executor = self._create_agent_executor()

#     def _create_tools(self):
#         tools = []
#         if self.vectorstore:
#             retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
#             knowledge_tool = Tool(
#                 name="stevens_knowledge_base",
#                 func=retriever,
#                 description="Search for information about Stevens Institute of Technology.",
#             )
#             tools.append(knowledge_tool)
#         return tools

#     def _get_vectorstore(self, use_faiss):
#         """Initialize or load the vector database"""
#         try:
#             embeddings = OpenAIEmbeddings()
#             if use_faiss and os.path.exists("faiss_index"):
#                 return FAISS.load_local("faiss_index", embeddings)
#             else:
#                 return None
#         except Exception as e:
#             print(f"Error loading vector store: {str(e)}")
#             return None

#     def _create_agent_executor(self):
#         """Create the agent executor with tools and memory"""
#         prompt = "You are StevensAI, a helpful assistant..."
#         agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=prompt)
#         return AgentExecutor(agent=agent, tools=self.tools, memory=self.memory)

#     def query(self, user_input):
#         """Process a user query and return the agent's response"""
#         try:
#             response = self.agent_executor.invoke({"input": user_input})
#             return response["output"]
#         except Exception as e:
#             return f"I encountered an error: {str(e)}."


# def get_simple_agent(api_key: str, use_faiss=True):
#     """Get or create a singleton agent instance"""
#     return SimpleStevensAgent(api_key=api_key, use_faiss=use_faiss)


# # Load environment variables
# load_dotenv()

# # Verify if the API key is loaded
# api_key = os.getenv("OPENAI_API_KEY")
# if api_key:
#     print("OpenAI API Key is set.")
# else:
#     raise ValueError("OpenAI API Key is not set. Please check your configuration.")

# # Create an agent instancess
# agent_instance = get_simple_agent(api_key)


# ------------------------------------------------------
# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain.memory import ConversationBufferMemory
# from langchain_community.vectorstores import FAISS
# from langchain.agents import (
#     AgentExecutor,
#     Tool,
#     create_react_agent,
#     AgentType,
#     initialize_agent,
# )
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

# # from langchain.agents.react.base import ReactAgent

# # Load API keys
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# class StevensChatbot:
#     def __init__(self):
#         """Initialize the chatbot with LLM, vector store, and tools."""
#         self.llm = ChatOpenAI(temperature=0.2)
#         self.memory = ConversationBufferMemory(
#             memory_key="chat_history", return_messages=True
#         )

#         # Load FAISS vector store
#         self.vectorstore = FAISS.load_local(
#             "faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True
#         )

#         # Create retrieval tool
#         retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
#         self.tools = [
#             Tool(
#                 name="Stevens Knowledge Base",
#                 func=retriever.get_relevant_documents,
#                 description="Fetch information about Stevens Institute of Technology.",
#             )
#         ]

#         # Define proper PromptTemplate
#         self.prompt = PromptTemplate(
#             input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
#             template="""
#             You are a knowledgeable AI assistant trained on information about Stevens Institute of Technology.

#             - If a user asks about **Stevens**, provide detailed, accurate answers.
#             - If a user asks an **irrelevant** question, simply reply: "This is not related to Stevens Institute Of Technology."
#             - If the question is about **critical topics** (fees, admissions, etc.), add this:
#               "[INFO]: Please contact the relevant department for more details."

#             Use OpenAI’s general knowledge when needed.

#             User: {input}
#             Thought: Let's analyze the question.
#             {agent_scratchpad}
#             Tools: {tools}
#             Tool Names: {tool_names}
#             Response:
#             """,
#         )

#         # Create LLM-powered agent
#         self.agent_executor = AgentExecutor(
#             agent=create_react_agent(
#                 llm=self.llm, tools=self.tools, prompt=self.prompt
#             ),
#             tools=self.tools,
#             memory=self.memory,
#             handle_parsing_errors=True,  # Handles any parsing issues automatically
#         )

#     def query(self, user_input):
#         """Process a user query and return the AI's response."""
#         try:
#             # Step 1: Ask OpenAI if the query is relevant to Stevens
#             relevance_check = self.llm.invoke(
#                 f"Is the following question related to Stevens Institute of Technology? Answer 'yes' or 'no' only.\n\nQuestion: {user_input}"
#             ).content.lower()

#             if "no" in relevance_check:
#                 return "This is not related to Stevens Institute Of Technology."

#             # Step 2: Get AI response
#             response = self.agent_executor.invoke({"input": user_input})["output"]

#             # Step 3: Check if the question is critical (fees, admissions, etc.)
#             critical_keywords = [
#                 "fees",
#                 "admission",
#                 "tuition",
#                 "scholarship",
#                 "financial aid",
#             ]
#             if any(keyword in user_input.lower() for keyword in critical_keywords):
#                 response = f"[INFO]: {response} Please contact the relevant department for more details."

#             return response
#         except Exception as e:
#             return f"❌ Error: {str(e)}"


# def get_stevens_agent():
#     """Create a chatbot instance."""
#     return StevensChatbot()


# try 3------------------------------------------------------------------------
# import os
# from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI, OpenAI
# from langchain.chains.llm import LLMChain
# from langchain.chains import RetrievalQA
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import re

# # Load API keys
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# class StevensAgent:
#     """AI agent for answering questions about Stevens Institute using FAISS and OpenAI."""

#     def __init__(self):
#         """Initialize the agent by loading the FAISS index and setting up the retrieval chain."""
#         self.embeddings = OpenAIEmbeddings()
#         self.db = FAISS.load_local("faiss_index", self.embeddings)  # Load FAISS index

#         self.retriever = self.db.as_retriever()
#         self.qa_chain = RetrievalQA.from_chain_type(
#             llm=OpenAI(model_name="gpt-4o", temperature=0), retriever=self.retriever
#         )  # Use GPT-4 for better formatting
#         self.prompt = PromptTemplate(
#             input_variables=["context", "question"],
#             template="""You are StevensAI, a helpful assistant trained on information about Stevens Institute of Technology.

#             If a user asks about **Stevens research labs**, provide a detailed, accurate list of labs based ONLY on the following context. If the context doesn't contain the names or information, explicitly say "I don't have complete information on the list of research labs in the context, but here is what I was able to identify:".  Do NOT use outside information.  Return your answer in  list format with "Research Lab Name" and "Description". Be as concise and give brief in the description. If there are more than 7 research labs, provide all of them.

#             If a user asks an **irrelevant** question, simply reply: "This is not related to Stevens Institute of Technology."

#             If the question is about **critical topics** (fees, admissions, etc.), add this: "[INFO]: Please contact the relevant department for more details."

#             If the question   is about **Stevens Latest News**, provide a brief news on the followimg context data. add this: "[INFO]: Please visit the Stevens News page for the latest updates."

#             Context: {context}

#             Question: {question}

#             Answer:
#             """,
#         )
#         self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

#     def load_vector_store(self, vector_store_path):
#         """Loads the FAISS vector store from the specified path."""
#         try:
#             embeddings = OpenAIEmbeddings()
#             db = FAISS.load_local(
#                 vector_store_path, embeddings, allow_dangerous_deserialization=True
#             )
#             print("✅ Vector store loaded successfully.")
#             return db
#         except Exception as e:
#             print(f"❌ Error loading vector store: {e}")
#             return None  # Or handle the error as appropriate

#     def query(self, query):
#         """Queries the vector store and returns an answer, or a default message."""
#         if not self.db:
#             return "❌ Vector store not loaded. Please ingest data first."

#         if not self.retriever:
#             return "❌ Retriever not initialized.  Check vector store loading."

#         # Fetch relevant documents
#         relevant_docs = self.retriever.get_relevant_documents(query)

#         if not relevant_docs:
#             return "This is not related to Stevens Institute Of Technology."

#         # Limit the number of documents to avoid exceeding context window
#         num_docs = min(5, len(relevant_docs))  # Or adjust this number
#         relevant_docs = relevant_docs[:num_docs]

#         context = "\n".join([doc.page_content for doc in relevant_docs])  # Combine docs

#         # Pass the question and combined context to the LLMChain
#         try:
#             response = self.llm_chain.invoke(
#                 {"context": context, "question": query}
#             )  # use invoke instead of run

#             # Basic cleaning - remove extra whitespace
#             response = response["text"].strip()  # Access output using "text"

#             # Check if the response contains lab names (crude check)
#             if (
#                 "lab" not in response.lower()
#                 and "I don't know" not in response.lower()
#                 and "I don't have information" not in response.lower()
#             ):
#                 return "I am unable to provide information"

#             return response  # Return the cleaned response

#         except Exception as e:
#             print(f"❌ Error during LLMChain run: {e}")
#             return "An error occurred while processing your request."


# -----------------------------------------------------------------------------------------
# try 5
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class StevensAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.db = FAISS.load_local(
            "faiss_index", self.embeddings, allow_dangerous_deserialization=True
        )
        self.retriever = self.db.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4o", temperature=0), retriever=self.retriever
        )

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
        You are StevensAI, the official AI assistant for Stevens Institute of Technology. Your purpose is to provide accurate, helpful information about Stevens to students, faculty, and visitors.

        Follow these principles in your responses:
        - ACCURACY: Base all answers ONLY on the provided context. If information is missing or incomplete, clearly state this limitation.
        - RELEVANCE: Only answer questions about Stevens Institute of Technology. For unrelated queries, respond: "This is not related to Stevens Institute of Technology."
        - TRANSPARENCY: Clearly indicate when information might be incomplete or when the user should seek official guidance.
        - HELPFULNESS: Structure your responses in a clear, concise manner that directly addresses the user's query.

        Response guidelines by topic:

        - GREETINGS:
        When the user greets you with "hi", "hello", "hey", "thanks", etc., respond with a warm welcome and ask what they’d like to know about Stevens Institute of Technology.

        - ACADEMICS:
        Share details about programs, departments, majors, courses, and academic policies.  
        For more information, visit: https://www.stevens.edu/academics

        - RESEARCH:
        Provide a structured list of Stevens research labs and initiatives, if present in the context.  
        For more info, refer to our Alex Agent.

        - CAMPUS LIFE:
        Mention housing, student life, dining, and campus amenities if available.  
        For more info, check this: https://www.stevens.edu/about

        - ADMISSIONS:
        Offer general info about the application process.  
        [INFO]: For specific admissions questions, please contact the Office of Admissions.  
        Learn more: https://www.stevens.edu/admissions

        - FINANCIAL MATTERS:
        When asked about tuition, fees, scholarships, or aid, provide available context.  
        [INFO]: Please contact the Office of Financial Aid or Student Accounts for the most current information.

        - INTERNATIONAL STUDENTS:
        Provide information on student support, F-1 status, airport pickup, etc., if mentioned.  
        For details, visit: https://www.stevens.edu/directory/international-student-and-scholar-services

        - EVENTS / NEWS:
        Share contextually available info and direct users to official updates.  
        [INFO]: Visit the Stevens News & Events page: https://www.stevens.edu/public-events

        - HISTORY / TRADITIONS:
        Mention key points about Stevens' founding, mission, and legacy.  
        For more, visit: https://www.stevens.edu/about

        - STUDENT RESOURCES:
        If user asks about graduate life, student services, travel, airport pickup, etc., provide what is in context.  
        For more info: https://www.stevens.edu/grad-student-resources

        - MAP / CAMPUS DIRECTIONS:
        Direct users to the campus map or travel resources.  
        Campus map: https://www.stevens.edu/about-stevens/campus-map  
        Travel info: https://www.stevens.edu/travel-information

        If you cannot find the answer in the context, respond with:  
        "I don't have complete information on that topic in the current context. Here's what I was able to find:"

        Always conclude with:  
        **For more info, you can check this link: [relevant page URL]**

        Context: {context}

        Question: {question}

        Answer:
            """,
        )

        self.llm_chain = LLMChain(
            llm=ChatOpenAI(model="gpt-4o", temperature=0.5), prompt=self.prompt
        )

    def get_response(self, user_query):
        if not self.db or not self.retriever:
            return "❌ Error: Vector store not initialized."

        try:
            # Step 1: Relevance check using LLM
            relevance_check = (
                ChatOpenAI(model="gpt-4o", temperature=0.5)
                .invoke(
                    f"Is the following question about Stevens Institute of Technology? Answer 'yes' or 'no'.\n\nQuestion: {user_query}"
                )
                .content.strip()
                .lower()
            )

            # if "no" in relevance_check:
            #     return "This is not related to Stevens Institute Of Technology."

            # Step 2: Get relevant documents
            relevant_docs = self.retriever.get_relevant_documents(user_query)
            context = "\n".join([doc.page_content for doc in relevant_docs[:5]])

            # Step 3: Generate response
            response = self.llm_chain.invoke(
                {"context": context, "question": user_query}
            )["text"].strip()

            # Step 4: Add advisory note if critical topic
            critical_keywords = [
                "fees",
                "admission",
                "tuition",
                "scholarship",
                "financial aid",
            ]
            if any(kw in user_query.lower() for kw in critical_keywords):
                response += "\n\n[INFO]: Please contact the relevant department for more details."
                print(response)

            return response

        except Exception as e:
            return f"❌ Error while generating response: {e}"
