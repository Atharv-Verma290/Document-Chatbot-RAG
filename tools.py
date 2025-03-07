from langchain_core.tools import tool

from constant import PERSIST_DIR, embeddings
from utils import get_vector_store

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    vector_store = get_vector_store()
    if vector_store is None:
        raise AttributeError('st.session_state has no attribute "vector_store". Did you forget to initialize it?')
    retrieved_docs =vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

