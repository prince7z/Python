from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


oai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")

)

def get_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Batch embed texts with OpenAI."""
    cleaned = [t.replace("\n", " ").strip() for t in texts]
    resp = oai.embeddings.create(input=cleaned, model=model)
    return [d.embedding for d in resp.data]

def get_embedding(text: str) -> List[float]:
    return get_embeddings([text])[0]