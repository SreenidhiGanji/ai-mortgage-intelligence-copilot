import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_embedding_for_text(text: str):
    """
    Generates one embedding vector for a single text input.
    """
    return embeddings_model.embed_query(text)


def generate_embeddings_for_documents(documents):
    """
    Generates embeddings for LangChain Document chunks.
    """
    texts = [doc.page_content for doc in documents]
    return embeddings_model.embed_documents(texts)