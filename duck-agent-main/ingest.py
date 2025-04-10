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

# import os
# import shutil
# import logging
# from dotenv import load_dotenv
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings

# # Load API Key
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if not OPENAI_API_KEY:
#     raise ValueError("❌ OPENAI_API_KEY not set. Please add it to your .env file.")

# # Setup logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # Define URLs
# urls = [
#     "https://www.stevens.edu/about",
#     "https://www.stevens.edu/academics",
#     "https://www.stevens.edu/admissions",
#     "https://www.stevens.edu/online-learning",
#     "https://thestute.com/",
#     "https://www.stevens.edu/public-events",
#     "https://www.stevens.edu/about-stevens/campus-map",
#     "https://www.stevens.edu/directory/graduate-academics/graduate-student-life-services",
#     "https://www.stevens.edu/directory/international-student-and-scholar-services",
#     "https://www.stevens.edu/page-basic/airport-pickup-service-for-new-graduate-students",
#     "https://www.stevens.edu/maintain-your-f-1-status",
#     "https://www.stevens.edu/travel-information",
#     "https://www.stevens.edu/discover-stevens/news",
#     "https://www.stevens.edu/grad-student-resources",
#     "https://www.stevens.edu/graduate-corporate-education",
# ]


# def ingest_data():
#     try:
#         logging.info("🔄 Loading data from URLs...")
#         loader = UnstructuredURLLoader(urls=urls)
#         documents = loader.load()

#         if not documents:
#             raise Exception(
#                 "No documents were loaded. Check the URLs or internet connection."
#             )

#         logging.info(f"✅ Loaded {len(documents)} documents.")

#         splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
#         texts = splitter.split_documents(documents)
#         logging.info(f"✅ Split into {len(texts)} chunks.")

#         embeddings = OpenAIEmbeddings()
#         db = FAISS.from_documents(texts, embeddings)
#         db.save_local("faiss_index")
#         logging.info("✅ FAISS vector store saved at 'faiss_index/'.")

#     except Exception as e:
#         logging.error(f"❌ Error during ingestion: {e}", exc_info=True)


# def clear_vector_store(path="faiss_index"):
#     try:
#         shutil.rmtree(path)
#         logging.info(f"✅ Cleared existing vector store at '{path}'.")
#     except FileNotFoundError:
#         logging.warning(f"⚠️ No vector store directory found at '{path}' to delete.")
#     except Exception as e:
#         logging.error(f"❌ Error deleting vector store: {e}")


# if __name__ == "__main__":
#     clear_vector_store()
#     ingest_data()

# 45 links Try---------------------------------------------------

# import os
# import shutil
# import logging
# from dotenv import load_dotenv
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings

# # Load API Key
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if not OPENAI_API_KEY:
#     raise ValueError("❌ OPENAI_API_KEY not set. Please add it to your .env file.")

# # Setup logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # Define URLs
# urls = [
#     "https://www.stevens.edu/about",
#     "https://www.stevens.edu/academics",
#     "https://www.stevens.edu/admissions",
#     "https://www.stevens.edu/online-learning",
#     "https://thestute.com/",
#     "https://www.stevens.edu/public-events",
#     "https://www.stevens.edu/about-stevens/campus-map",
#     "https://www.stevens.edu/directory/graduate-academics/graduate-student-life-services",
#     "https://www.stevens.edu/directory/international-student-and-scholar-services",
#     "https://www.stevens.edu/page-basic/airport-pickup-service-for-new-graduate-students",
#     "https://www.stevens.edu/maintain-your-f-1-status",
#     "https://www.stevens.edu/travel-information",
#     "https://www.stevens.edu/discover-stevens/news",
#     "https://www.stevens.edu/grad-student-resources",
#     "https://www.stevens.edu/graduate-corporate-education",
#     "https://www.stevens.edu/campus-life/residence-life",
#     "https://www.stevens.edu/campus-life/dining-services",
#     "https://www.stevens.edu/campus-life/health-wellness",
#     "https://www.stevens.edu/transportation-and-parking/stevens-shuttle",
#     "https://www.stevens.edu/transportation-and-parking/nj-transit",
#     "https://www.stevens.edu/page-basic/public-transportation",
#     "https://www.stevens.edu/campus-life/diversity-inclusion",
#     "https://www.stevens.edu/off-campus-employment/isss-f1-students/cpt-work-authorization",
#     "https://www.stevens.edu/cpt-frequently-asked-questions",
#     "https://www.stevens.edu/academics/graduate-study/academic-policies-and-procedures#policies-procedures-a-i",
#     "https://www.stevens.edu/academics/graduate-study/academic-policies-and-procedures#policies-procedures-j-r",
#     "https://www.stevens.edu/academics/graduate-study/academic-policies-and-procedures#policies-procedures-s-z",
#     "https://www.stevens.edu/academics/graduate-study/graduate-student-handbook",
#     "https://www.stevens.edu/admission-aid/undergraduate-admissions/new-students/health-and-immunization-requirements",
#     "https://www.stevens.edu/counseling-psychological-services",
#     "https://www.stevens.edu/apply-i20",
#     "https://www.stevens.edu/financial-documentation-requirements-newly-admitted"
#     "https://www.stevens.edu/cpt-frequently-asked-questions",
#     "https://www.stevens.edu/off-campus-employment/isss-f1-students/cpt-work-authorization",
#     "https://www.stevens.edu/information-for-parents-and-families",
#     "https://www.stevens.edu/policies-library",
#     "https://www.stevens.edu/academics/stevensonline/stevens-online",
#     "https://www.stevens.edu/discover-stevens/leadership-and-vision",
#     "https://www.stevens.edu/discover-stevens/leadership-and-vision/the-presidents-leadership-council",
#     "https://www.stevens.edu/discover-stevens/leadership-and-vision/office-president",
#     "https://www.stevens.edu/discover-stevens/leadership-and-vision/board-of-trustees",
#     "https://www.stevens.edu/office-of-the-provost",
#     "https://www.stevens.edu/admission-aid/graduate-admissions/chat-with-a-student",
#     "https://www.stevens.edu/academics/graduate-study/graduate-funding/assistantships-and-fellowships",
#     "https://www.stevens.edu/admission-aid/graduate-admissions/graduate-programs/graduate-degrees-and-programs",
#     "https://www.stevens.edu/admission-aid/tuition-financial-aid/graduate-costs-and-funding",
#     "https://www.stevens.edu/tuition-fees-and-costs",
#     "https://www.stevens.edu/admissions-aid/graduate-admissions/acceptance-categories",
# ]


# def ingest_data():
#     try:
#         logging.info("🔄 Loading data from URLs...")
#         loader = UnstructuredURLLoader(urls=urls)
#         documents = loader.load()

#         if not documents:
#             raise Exception(
#                 "No documents were loaded. Check the URLs or internet connection."
#             )

#         logging.info(f"✅ Loaded {len(documents)} documents.")

#         splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
#         texts = splitter.split_documents(documents)
#         logging.info(f"✅ Split into {len(texts)} chunks.")

#         embeddings = OpenAIEmbeddings()
#         db = FAISS.from_documents(texts, embeddings)
#         db.save_local("faiss_index")
#         logging.info("✅ FAISS vector store saved at 'faiss_index/'.")

#     except Exception as e:
#         logging.error(f"❌ Error during ingestion: {e}", exc_info=True)


# def clear_vector_store(path="faiss_index"):
#     try:
#         shutil.rmtree(path)
#         logging.info(f"✅ Cleared existing vector store at '{path}'.")
#     except FileNotFoundError:
#         logging.warning(f"⚠️ No vector store directory found at '{path}' to delete.")
#     except Exception as e:
#         logging.error(f"❌ Error deleting vector store: {e}")


# if __name__ == "__main__":
#     clear_vector_store()
#     ingest_data()

# More links ---------------------------------------------------


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

# import os
# import shutil
# import logging
# from dotenv import load_dotenv
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings

# # Load API Key
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if not OPENAI_API_KEY:
#     raise ValueError("❌ OPENAI_API_KEY not set. Please add it to your .env file.")

# # Setup logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # Define URLs
# urls = [
#     "https://www.stevens.edu/about",
#     "https://www.stevens.edu/academics",
#     "https://www.stevens.edu/admissions",
#     "https://www.stevens.edu/online-learning",
#     "https://thestute.com/",
#     "https://www.stevens.edu/public-events",
#     "https://www.stevens.edu/about-stevens/campus-map",
#     "https://www.stevens.edu/directory/graduate-academics/graduate-student-life-services",
#     "https://www.stevens.edu/directory/international-student-and-scholar-services",
#     "https://www.stevens.edu/page-basic/airport-pickup-service-for-new-graduate-students",
#     "https://www.stevens.edu/maintain-your-f-1-status",
#     "https://www.stevens.edu/travel-information",
#     "https://www.stevens.edu/discover-stevens/news",
#     "https://www.stevens.edu/grad-student-resources",
#     "https://www.stevens.edu/graduate-corporate-education",
# ]


# def ingest_data():
#     try:
#         logging.info("🔄 Loading data from URLs...")
#         loader = UnstructuredURLLoader(urls=urls)
#         documents = loader.load()

#         if not documents:
#             raise Exception(
#                 "No documents were loaded. Check the URLs or internet connection."
#             )

#         logging.info(f"✅ Loaded {len(documents)} documents.")

#         splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
#         texts = splitter.split_documents(documents)
#         logging.info(f"✅ Split into {len(texts)} chunks.")

#         embeddings = OpenAIEmbeddings()
#         db = FAISS.from_documents(texts, embeddings)
#         db.save_local("faiss_index")
#         logging.info("✅ FAISS vector store saved at 'faiss_index/'.")

#     except Exception as e:
#         logging.error(f"❌ Error during ingestion: {e}", exc_info=True)


# def clear_vector_store(path="faiss_index"):
#     try:
#         shutil.rmtree(path)
#         logging.info(f"✅ Cleared existing vector store at '{path}'.")
#     except FileNotFoundError:
#         logging.warning(f"⚠️ No vector store directory found at '{path}' to delete.")
#     except Exception as e:
#         logging.error(f"❌ Error deleting vector store: {e}")


# if __name__ == "__main__":
#     clear_vector_store()
#     ingest_data()

# Last Try---------------------------------------------------

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
    "https://www.stevens.edu/campus-life/residence-life",
    "https://www.stevens.edu/campus-life/dining-services",
    "https://www.stevens.edu/campus-life/health-wellness",
    "https://www.stevens.edu/transportation-and-parking/stevens-shuttle",
    "https://www.stevens.edu/transportation-and-parking/nj-transit",
    "https://www.stevens.edu/page-basic/public-transportation",
    "https://www.stevens.edu/campus-life/diversity-inclusion",
    "https://www.stevens.edu/off-campus-employment/isss-f1-students/cpt-work-authorization",
    "https://www.stevens.edu/cpt-frequently-asked-questions",
    "https://www.stevens.edu/academics/graduate-study/academic-policies-and-procedures#policies-procedures-a-i",
    "https://www.stevens.edu/academics/graduate-study/academic-policies-and-procedures#policies-procedures-j-r",
    "https://www.stevens.edu/academics/graduate-study/academic-policies-and-procedures#policies-procedures-s-z",
    "https://www.stevens.edu/academics/graduate-study/graduate-student-handbook",
    "https://www.stevens.edu/admission-aid/undergraduate-admissions/new-students/health-and-immunization-requirements",
    "https://www.stevens.edu/counseling-psychological-services",
    "https://www.stevens.edu/apply-i20",
    "https://www.stevens.edu/financial-documentation-requirements-newly-admitted",
    "https://www.stevens.edu/cpt-frequently-asked-questions",
    "https://www.stevens.edu/off-campus-employment/isss-f1-students/cpt-work-authorization",
    "https://www.stevens.edu/information-for-parents-and-families",
    "https://www.stevens.edu/policies-library",
    "https://www.stevens.edu/academics/stevensonline/stevens-online",
    "https://www.stevens.edu/discover-stevens/leadership-and-vision",
    "https://www.stevens.edu/discover-stevens/leadership-and-vision/the-presidents-leadership-council",
    "https://www.stevens.edu/discover-stevens/leadership-and-vision/office-president",
    "https://www.stevens.edu/discover-stevens/leadership-and-vision/board-of-trustees",
    "https://www.stevens.edu/office-of-the-provost",
    "https://www.stevens.edu/admission-aid/graduate-admissions/chat-with-a-student",
    "https://www.stevens.edu/academics/graduate-study/graduate-funding/assistantships-and-fellowships",
    "https://www.stevens.edu/admission-aid/graduate-admissions/graduate-programs/graduate-degrees-and-programs",
    "https://www.stevens.edu/admission-aid/tuition-financial-aid/graduate-costs-and-funding",
    "https://www.stevens.edu/tuition-fees-and-costs",
    "https://www.stevens.edu/admissions-aid/graduate-admissions/acceptance-categories",
    "https://stevensducks.com/",
    "https://www.stevens.edu/page-minisite-landing/student-health-services",
    "https://www.stevens.edu/student-health-services/health-and-immunization-records",
    "https://www.stevens.edu/student-health-services/on-campus-covid-19-vaccination",
    "https://www.stevens.edu/student-health-services/flu-shots",
    "https://www.stevens.edu/student-health-insurance-plan-information",
    "https://stevensrec.com/",
    "https://stevensrec.com/sports/facilities",
    "https://www.stevens.edu/graduate-education/english-language-proficiency-policy",
    "https://www.stevens.edu/discover-stevens/stevens-by-the-numbers/rankings-recognition"
    "https://www.stevens.edu/discover-stevens/stevens-by-the-numbers/facts-statistics",
    "https://stevens.bncollege.com/",
    "https://www.stevens.edu/development-alumni-engagement/connect/stevens-alumni-award-recipients",
    "https://www.stevens.edu/development-alumni-engagement/development-alumni-news",
    "https://www.stevens.edu/career-center/career-coaching",
    "https://www.stevens.edu/admission-aid/graduate-admissions/graduate-events-and-open-houses",
    "https://www.stevens.edu/page-right-nav/visit-visitor-parking",
    "https://www.stevens.edu/visit/nearby-airports",
    "https://www.stevens.edu/gender-inclusive-restrooms",
    "https://www.stevens.edu/info-for/why-stevens",
    "https://www.stevens.edu/student-employment-office",
    "https://www.stevens.edu/discover-stevens/diversity-equity-inclusion",
    "https://www.stevens.edu/emergency-information",
    "https://www.stevens.edu/campus-safety",
    "https://www.stevens.edu/division-of-facilities-and-campus-operations/campus-police/fire-safety",
    "https://www.stevens.edu/campus-police/what-to-do-if-an-active-shooter-event-takes-place-on-campus",
    "https://www.stevens.edu/page-right-nav/how-to-report-a-crime",
    "https://www.stevens.edu/admission-aid/undergraduate-admissions/new-students/information-and-events-for-parents-and-families",
    "https://www.stevens.edu/student-life/the-stevens-experience/mental-health-concerns-how-and-when-should-i-help-intro",
    "https://www.stevens.edu/school-engineering-science/about",
    "https://www.stevens.edu/school-engineering-science/departments",
    "https://www.stevens.edu/school-engineering-science/graduate-studies/programs",
    "https://stevens.smartcatalogiq.com/en/2023-2024/academic-catalog/student-services/disability-services/",
    "https://stevens.smartcatalogiq.com/en/2023-2024/academic-catalog/student-services/living-at-stevens/on-campus-housing/",
    "https://dineoncampus.com/stevensdining/student-meal-plans/",
    "https://dineoncampus.com/stevensdining/feed-the-flock",
    "https://dineoncampus.com/stevensdining/mobile-ordering",
    "https://dineoncampus.com/stevensdining/grubhub-",
    "https://dineoncampus.com/stevensdining/stevens-dining-offices",
    "https://www.stevens.edu/duck-card-services",
    "https://www.stevens.edu/temporary-housing-for-graduate-students",
    "https://www.stevens.edu/student-life/the-stevens-experience/living-at-stevens/dining-at-stevens",
    "https://library.stevens.edu/borrow/policies",
    "https://library.stevens.edu/libraryhours",
    "https://stevens.libcal.com/r/new",
    "https://library.stevens.edu/librarytech#s-lg-box-31225843",
    "https://www.stevens.edu/student-life/commencement",
    "https://www.stevens.edu/discover-stevens/strategic-plan",
    "https://gradcs-courses.tiiny.site",
    "https://www.stevens.edu/it/services",
    "https://www.stevens.edu/it/resources/student-digital-backpack",
    "https://www.stevens.edu/it/resources",
    "https://stevens.smartcatalogiq.com/en/2023-2024/academic-catalog/tuition-fees-and-other-expenses-for-graduate-students/payment-options/",
    "https://www.stevens.edu/office-of-student-accounts/charge-adjustment-schedule",
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
