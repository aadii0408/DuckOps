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


# --------------------------------------------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# URLs to scrape
urls = [
    "https://www.stevens.edu/about",
    "https://www.stevens.edu/academics",
    "https://www.stevens.edu/campus-life",
    "https://www.stevens.edu/admissions",
    "https://www.stevens.edu/research",
]

def ingest_data():
    """Fetches data from Stevens URLs, processes it, and stores embeddings."""
    print("🔄 Loading data from Stevens website...")
    
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    print(f"✅ Processed {len(texts)} text chunks.")

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    db.save_local("faiss_index")  # Save for retrieval
    print("✅ FAISS vector store saved successfully.")

if __name__ == "__main__":
    ingest_data()
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# URLs to scrape
urls = [
    "https://www.stevens.edu/about",
    "https://www.stevens.edu/academics",
    "https://www.stevens.edu/campus-life",
    "https://www.stevens.edu/admissions",
    "https://www.stevens.edu/research",
]

def ingest_data():
    """Fetches data from Stevens URLs, processes it, and stores embeddings."""
    print("🔄 Loading data from Stevens website...")
    
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    print(f"✅ Processed {len(texts)} text chunks.")

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    db.save_local("faiss_index")  # Save for retrieval
    print("✅ FAISS vector store saved successfully.")

if __name__ == "__main__":
    ingest_data()
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# URLs to scrape
urls = [
    "https://www.stevens.edu/about",
    "https://www.stevens.edu/academics",
    "https://www.stevens.edu/campus-life",
    "https://www.stevens.edu/admissions",
    "https://www.stevens.edu/research",
]


def ingest_data():
    """Fetches data from Stevens URLs, processes it, and stores embeddings."""
    print("🔄 Loading data from Stevens website...")

    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    print(f"✅ Processed {len(texts)} text chunks.")

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    db.save_local("faiss_index")  # Save for retrieval
    print("✅ FAISS vector store saved successfully.")


if __name__ == "__main__":
    ingest_data()
