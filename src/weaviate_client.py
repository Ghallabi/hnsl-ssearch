import weaviate
import weaviate.classes.config as wvcc
import weaviate.classes as wvc
import weaviate.classes as wvc
import src.env as env


class WeaviateClient:

    def __init__(self):
        self.client = weaviate.connect_to_custom(
            http_host=env.WEAVIATE_HTTP_HOST,
            grpc_host=env.WEAVIATE_GRPC_HOST,
            http_port=env.WEAVIATE_HTTP_PORT,
            http_secure=env.WEAVIATE_HTTP_SECURE,
            grpc_port=env.WEAVIATE_GRPC_PORT,
            grpc_secure=env.WEAVIATE_GRPC_SECURE,
            auth_credentials=env.WEAVIATE_AUTH_CRED,
        )
        self.collection = self.client.collections.get(env.WEAVIATE_COLECTION_NAME)
        self.properties = [prop for prop in env.WEAVIATE_QUERY_PROPERTIES]

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
        class_uuid: str,
    ):
        print(f"Inserting new item with class uuid {class_uuid}")
        self.collection.data.insert(
            properties={
                "Title": title,
                "url": url,
            },
            vector=embedding.tolist(),
        )
