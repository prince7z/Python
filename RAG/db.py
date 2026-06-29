
import chromadb

chroma = chromadb.Client()
collection = chroma.create_collection("naive_rag", metadata={"hnsw:space": "cosine"})
