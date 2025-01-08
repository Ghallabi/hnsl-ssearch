from sentence_transformers import SentenceTransformer
from .utils import create_corpus_chunks
import torch


class STextEmbedder:
    def __init__(
        self,
        embedder_name: str = "all-MiniLM-L6-v2",
        max_length: int = 128,
        overlap: int = 20,
        device=torch.device("cpu"),
    ):
        self.embedder = SentenceTransformer(embedder_name, device=device)
        self.max_length = max_length
        self.overlap = overlap

    def embed(self, corpus) -> torch.Tensor:
        chunks = create_corpus_chunks(corpus, self.max_length, self.overlap)
        embeddings = self.embedder.encode(chunks, convert_to_tensor=True)
        return embeddings

    def embed_query(self, query: str) -> torch.Tensor:
        query_embedding = self.embedder.encode(query)
        return query_embedding
