from pathlib import Path
from uuid import uuid4
import pandas as pd
from src.embed import STextEmbedder
from src.weaviate_client import WeaviateClient
import src.env as env


def index_from_csv(csv_file: Path, wv_client):
    df = pd.read_csv(csv_file)
    embedder = STextEmbedder(embedder_name=env.EMBEDDER_NAME, device=env.DEVICE)
    for index, row in df.iterrows():
        filename = row["title"].lower().replace(" ", "_")
        filename = filename.replace(".", "_")
        try:
            with open(f"./data/contents/{filename}.txt", "r") as f:
                corpus = f.read()
            embeddings = embedder.embed(corpus)
            for embedding in embeddings:
                chunk_uuid = uuid4()
                wv_client.add_new_item(
                    embedding, title=row["title"], url=row["url"], chunk_uuid=chunk_uuid
                )
            if index % 100 == 0:
                print(f"Finished indexing URL {index} / {len(df)}")
        except Exception as e:
            pass


if __name__ == "__main__":
    csv_file = Path().cwd() / "data/yamrzou_links.csv"
    wv_client = WeaviateClient()
    index_from_csv(csv_file, wv_client)
