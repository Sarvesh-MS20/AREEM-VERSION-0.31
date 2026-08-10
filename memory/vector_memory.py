#memory/vector_memory.py
# -------------------------------------------------------------------------------------------
#                              CREATING A VECTOR MEMORY
# -------------------------------------------------------------------------------------------
import faiss
import numpy as np
from rag.retriever import embed_model

memory_text = []
memory_embedding =[]

#creating a memory brain
def add_memory(text):
    global memory_text,memory_embedding
    emb = embed_model(text)
    faiss.normalize_l2(emb)
    memory_text.append(text)
    memory_embedding.append(emb[0])  #“The model returns a list of embeddings, so for a single input I take the first element to get the actual vector.”


# adding info to the brain
def build_memory():
    if not memory_embedding:
        return []

    emb = np.array(memory_embedding)
    dim = emb.shape[1]
    mem_index = faiss.IndexFlatL2(dim)
    mem_index.add(emb)
    return mem_index

# exatracting the info
def extract_memory(query,k=3):
    if not memory_embedding:
        return []

    mem_index = build_memory()
    query_emb = embed_model.encode([query])
    faiss.normalize_L2(query_emb)
    D,I= mem_index.search(query_emb,k)
    result= [memory_text[i] for i in I[0]]
    return result





