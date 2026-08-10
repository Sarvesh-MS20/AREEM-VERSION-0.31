#rag/retriever.py
from sentence_transformers import SentenceTransformer
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import faiss
import numpy as np

# ------------------------------------------------------
#                   DATA LOADING
# ------------------------------------------------------
data = open('DATA.txt').read().lower()
sentences = sent_tokenize(data)                     #seperating into sentences


# ------------------------------------------------------
#                   EMBEDDING MODEL
# ------------------------------------------------------
embed_model = SentenceTransformer('all-miniLM-L6-v2')
embeddings = embed_model.encode(sentences)


# ------------------------------------------------------
#                   FAISS
# ------------------------------------------------------

faiss.normalize_L2(embeddings)
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(np.array(embeddings))



# ------------------------------------------------------
#                   RETRIEVAL
# ------------------------------------------------------
def retriever(query,k=3):
    query_embed = embed_model.encode([query])
    faiss.normalize_L2(query_embed)
    D,I =index.search(query_embed,k)
    if D[0][0]<0.5:
        return []
    result = [sentences[i] for i in I[0]]
    return result




