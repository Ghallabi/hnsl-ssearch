import weaviate
import weaviate.classes as wvc
import weaviate.classes.config as wc
import src.env as env


class WeaviateClient:
    def __init__(self):
        self.client = weaviate.connect_to_local()
        if not self.client.collections.exists(env.WEAVIATE_COLLECTION_NAME):
            print("Collection doesn't exist - Creating it")
            self.client.collections.create(
                name=env.WEAVIATE_COLLECTION_NAME,
                properties=[
                    wc.Property(name="title", data_type=wc.DataType.TEXT),
                    wc.Property(name="url", data_type=wc.DataType.TEXT),
                    wc.Property(name="chunk_uuid", data_type=wc.DataType.UUID),
                ],
            )

        self.collection = self.client.collections.get(env.WEAVIATE_COLLECTION_NAME)
        self.properties = ["title", "url", "chunk_uuid"]

    def query(self, query_embedding):
        result = self.collection.query.near_vector(
            near_vector=query_embedding.tolist(),
            limit=env.MAX_RETRIEVED,
            return_metadata=wvc.query.MetadataQuery(certainty=True),
            return_properties=self.properties,
        )
        return result

    def add_new_item(
        self,
        embedding,
        title: str,
        url: str,
        chunk_uuid: str,
    ):
        self.collection.data.insert(
            properties={"Title": title, "url": url, "chunk_uuid": chunk_uuid},
            vector=embedding.tolist(),
        )
