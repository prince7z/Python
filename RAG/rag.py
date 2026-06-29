# --- The naive RAG query function ---
from emb import get_embedding
from db import collection

def naive_rag(question: str, k: int = 5, verbose: bool = True) -> str:
    """Simplest RAG: semantic search → stuff prompt → generate."""

    results = collection.query(
        query_embeddings=[get_embedding(question)],
        n_results=k
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    if verbose:
        print(f"\n🔍 Query: '{question}'")
        print(f"\nRetrieved {k} chunks:")
        for i, (d, m, dist) in enumerate(zip(docs, metas, dists)):
            print(f"  [{i+1}] dist={dist:.3f} | {m['title']}")
            print(f"      {d[:80]}...")

    context = "\n".join(
        f"[Source: {m['title']}]\n{d}" for d, m in zip(docs, metas)
    )

    resp = oai.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role": "user", "content": f"""Answer based ONLY on the context below.
If the context doesn't have the answer, say \"I don't have enough information.\"
Cite your sources.

Context:
{context}

Question: {question}

Answer:"""}]
    )

    answer = resp.choices[0].message.content
    if verbose:
        print(f"\n💬 Answer:\n{answer}")
    return answer