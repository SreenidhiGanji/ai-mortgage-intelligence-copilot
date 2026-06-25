from src.vector_store import load_vector_store


def retrieve_relevant_documents(query: str, k: int = 5):
    """
    Retrieves the most relevant mortgage document chunks from ChromaDB.
    """
    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": k
        }
    )

    documents = retriever.invoke(query)

    return documents