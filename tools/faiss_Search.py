#tools/faiss_search.py
from rag.retriever import retriever
# for retrieval (RAG)
def faiss_search(query):
    context = retriever(query)
    if not context:
        return ("NO_CONTEXT")
    return " ".join(context)
