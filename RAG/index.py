from emb import get_embeddings
from docs import DOCUMENTS
from chunking import chunk_recursive
from rag import naive_rag
from dotenv import load_dotenv
from db import chroma, collection
import os

load_dotenv()

os.environ["OPENAI_API_KEY"]  = os.getenv("OPENAI_API_KEY")


# --- Chunk all documents ---

all_chunks = []
chunk_meta = []

for doc in DOCUMENTS:
    chunks = chunk_recursive(doc["content"], max_size=100)
    for chunk in chunks:
        all_chunks.append(chunk)
        chunk_meta.append({"title": doc["title"], "source": doc["source"]})

print(f"Total chunks: {len(all_chunks)}")
for doc in DOCUMENTS:
    n = sum(1 for m in chunk_meta if m["title"] == doc["title"])
    print(f"  {doc['title']}: {n} chunks")


# --- Embed and store in ChromaDB ---


try: chroma.delete_collection("naive_rag")
except: pass

collection = chroma.create_collection("naive_rag", metadata={"hnsw:space": "cosine"})

embs = get_embeddings(all_chunks)

collection.add(
    ids=[f"chunk_{i}" for i in range(len(all_chunks))],
    embeddings=embs,
    documents=all_chunks,
    metadatas=chunk_meta
)

print(f"✅ Stored {len(all_chunks)} chunks in ChromaDB")   


answer = naive_rag("What is Prince Sahu's professional focus?,wht is his stack", k=3, verbose=True) 
print(f"\n\nFinal Answer:\n{answer}")
