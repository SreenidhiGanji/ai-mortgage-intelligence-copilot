import os
from dotenv import load_dotenv
from openai import OpenAI

from src.retrieval_service import retrieve_relevant_documents

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def build_context(documents) -> str:
    """
    Combines retrieved documents into a single context block.
    """
    context_parts = []

    for index, doc in enumerate(documents, start=1):
        context_parts.append(
            f"Document {index}:\n{doc.page_content}"
        )

    return "\n\n".join(context_parts)


def answer_mortgage_question(question: str) -> str:
    """
    Uses retrieved HMDA mortgage documents to answer the user's question.
    """
    retrieved_docs = retrieve_relevant_documents(question, k=5)
    context = build_context(retrieved_docs)

    prompt = f"""
You are an AI mortgage intelligence copilot.

Use ONLY the provided HMDA mortgage context to answer the user's question.
Do not make up facts.
If the context is not enough, say that the available data is limited.

Context:
{context}

User Question:
{question}

Answer in clear business language.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text