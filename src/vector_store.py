from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

PERSIST_DIRECTORY = "chroma_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")
)

def create_vector_store(documents):
    """
    Creates a persistent ChromaDB vector store from document chunks.
    """
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    return vector_store

def load_vector_store():
    """
    Loads existing ChromaDB vector store.
    """
    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    return vector_store


def semantic_search(query: str, k: int = 5):
    """
    Searches ChromaDB for mortgage document chunks similar to the user query.
    """
    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        query,
        k=k
    )

    return results