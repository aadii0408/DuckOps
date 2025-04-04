# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # Load environment variables
# load_dotenv()

# # Verify if the API key is loaded
# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise ValueError("❌ OpenAI API Key is not set. Please check your .env file.")

# print("✅ OpenAI API Key is set.")
# import os
# from dotenv import load_dotenv
# from pydantic import BaseModel

# # Load environment variables
# load_dotenv()


# class Config(BaseModel):
#     api_key: str

#     def __get_pydantic_json_schema__(self, *args, **kwargs):
#         return super().__get_pydantic_json_schema__(*args, **kwargs)


# # Verify if the API key is loaded
# config = Config(api_key=os.getenv("OPENAI_API_KEY"))
# if not config.api_key:
#     raise ValueError("❌ OpenAI API Key is not set. Please check your .env file.")

# print("✅ OpenAI API Key is set.")


# def ingest_documents(use_faiss=True):
#     """
#     Ingest documents from Stevens Institute website URLs and create a FAISS vector store or use in-memory storage.
#     """
#     urls = [
#         "https://www.stevens.edu/about",
#         "https://www.stevens.edu/academics",
#         "https://www.stevens.edu/campus-life",
#         "https://www.stevens.edu/admissions",
#         "https://www.stevens.edu/research",
#     ]

#     try:
#         print(f"🔄 Loading data from {len(urls)} URLs...")
#         loader = UnstructuredURLLoader(urls=urls)
#         documents = loader.load()

#         if not documents:
#             raise ValueError("❌ No documents loaded. Please check the URLs.")

#         print(f"✅ Loaded {len(documents)} documents.")

#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000, chunk_overlap=200
#         )
#         texts = text_splitter.split_documents(documents)

#         if not texts:
#             raise ValueError("❌ No text chunks created after splitting.")

#         print(f"✅ Split into {len(texts)} chunks.")

#         embeddings = OpenAIEmbeddings()

#         if use_faiss:
#             db = FAISS.from_documents(texts, embeddings)
#             os.makedirs("faiss_index", exist_ok=True)
#             db.save_local("faiss_index")
#             print("✅ FAISS index saved successfully in 'faiss_index/'.")
#         else:
#             # In-memory storage option (without persistent database)
#             print("✅ In-memory storage created; no database will be used.")

#     except Exception as e:
#         print(f"❌ Error during document ingestion: {str(e)}")


# if __name__ == "__main__":
#     ingest_documents(use_faiss=True)  # Change to False for in-memory only


# try 4 -------------------------------------------------------------------------------------------------------------------
# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# import shutil
# import logging  # Import the logging module
# import time

# # Configure logging (optional, but helpful for debugging)
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # Load API keys
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # URLs to scrape
# urls = [
#     "https://www.stevens.edu/about",
#     "https://www.stevens.edu/academics",
#     # "https://www.stevens.edu/campus-life",
#     "https://www.stevens.edu/admissions",
#     "https://www.stevens.edu/online-learning",
#     "https://thestute.com/",
#     "https://www.stevens.edu/public-events",
# ]


# def ingest_data():
#     """Fetches data from Stevens URLs, processes it, and stores embeddings."""
#     print("🔄 Loading data from Stevens website...")
#     logging.info("Starting data ingestion process.")  # Log the start

#     try:
#         loader = UnstructuredURLLoader(urls=urls)
#         documents = loader.load()  # Load all documents at once

#         # Log document loading success
#         logging.info(f"Successfully loaded {len(documents)} documents.")

#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1500, chunk_overlap=300
#         )  # Adjusted chunk size and overlap

#         texts = text_splitter.split_documents(documents)

#         # Log success of splitting
#         logging.info(f"Split documents into {len(texts)} text chunks.")

#         print(f"✅ Processed {len(texts)} text chunks.")

#         embeddings = OpenAIEmbeddings()
#         db = FAISS.from_documents(texts, embeddings)

#         db.save_local("faiss_index")  # Save for retrieval
#         print("✅ FAISS vector store saved successfully.")
#         logging.info("FAISS vector store saved successfully.")  # Log the save

#     except Exception as e:
#         print(f"❌ Error during data ingestion: {e}")
#         logging.error(
#             f"Error during data ingestion: {e}", exc_info=True
#         )  # Log the error


# def clear_vector_store(directory="faiss_index"):
#     """Clears the FAISS vector store directory."""
#     try:
#         shutil.rmtree(directory)
#         print(f"✅ Successfully cleared the vector store at '{directory}'.")
#     except FileNotFoundError:
#         print(
#             f"⚠️ Vector store directory '{directory}' not found.  It may not exist yet."
#         )
#     except Exception as e:
#         print(f"❌ Error clearing vector store: {e}")


# if __name__ == "__main__":
#     # clear_vector_store() #Uncomment this line to clear the vector store
#     ingest_data()

import os
import shutil
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not set. Please add it to your .env file.")

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define URLs
urls = [
    "https://www.stevens.edu/about",
    "https://www.stevens.edu/academics",
    "https://www.stevens.edu/admissions",
    "https://www.stevens.edu/online-learning",
    "https://thestute.com/",
    "https://www.stevens.edu/public-events",
    "https://www.stevens.edu/about-stevens/campus-map",
    "https://www.stevens.edu/directory/graduate-academics/graduate-student-life-services",
    "https://www.stevens.edu/directory/international-student-and-scholar-services",
    "https://www.stevens.edu/page-basic/airport-pickup-service-for-new-graduate-students",
    "https://www.stevens.edu/maintain-your-f-1-status",
    "https://www.stevens.edu/travel-information",
    "https://www.stevens.edu/discover-stevens/news",
    "https://www.stevens.edu/grad-student-resources",
    "https://www.stevens.edu/graduate-corporate-education",
]


def ingest_data():
    try:
        logging.info("🔄 Loading data from URLs...")
        loader = UnstructuredURLLoader(urls=urls)
        documents = loader.load()

        if not documents:
            raise Exception(
                "No documents were loaded. Check the URLs or internet connection."
            )

        logging.info(f"✅ Loaded {len(documents)} documents.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
        texts = splitter.split_documents(documents)
        logging.info(f"✅ Split into {len(texts)} chunks.")

        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(texts, embeddings)
        db.save_local("faiss_index")
        logging.info("✅ FAISS vector store saved at 'faiss_index/'.")

    except Exception as e:
        logging.error(f"❌ Error during ingestion: {e}", exc_info=True)


def clear_vector_store(path="faiss_index"):
    try:
        shutil.rmtree(path)
        logging.info(f"✅ Cleared existing vector store at '{path}'.")
    except FileNotFoundError:
        logging.warning(f"⚠️ No vector store directory found at '{path}' to delete.")
    except Exception as e:
        logging.error(f"❌ Error deleting vector store: {e}")


if __name__ == "__main__":
    clear_vector_store()
    ingest_data()
