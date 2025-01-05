def create_corpus_chunks(text, max_length: int = 128, overlap: int = 20) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_length, len(words))
        chunk = " ".join(words[start:end])
        start += max_length - overlap
        chunks.append(chunk)
    return chunks
