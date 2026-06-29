# --- Strategy 2: Recursive/Semantic (split on natural boundaries) ---

def chunk_recursive(text: str, max_size: int = 200) -> List[str]:
    """Split text on natural boundaries: paragraphs, then sentences."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    for para in paragraphs:
        words = para.split()
        if len(words) <= max_size:
            chunks.append(para)
        else:
            sentences = para.replace(". ", ".\n").split("\n")
            current, current_len = [], 0
            for sent in sentences:
                sent_len = len(sent.split())
                if current_len + sent_len > max_size and current:
                    chunks.append(" ".join(current))
                    current, current_len = [sent], sent_len
                else:
                    current.append(sent)
                    current_len += sent_len
            if current:
                chunks.append(" ".join(current))

    return [c for c in chunks if len(c.split()) > 10]