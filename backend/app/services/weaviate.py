from weaviate import Client

class WeaviateService:
    def __init__(self, weaviate_url: str):
        self.client = Client(weaviate_url)

    def create_class(self, class_name: str, properties: dict):
        self.client.schema.create_class({
            "class": class_name,
            "properties": properties
        })

    def delete_class(self, class_name: str):
        self.client.schema.delete_class(class_name)

    def add_object(self, class_name: str, object_data: dict):
        self.client.data_object.create(object_data, class_name)

    def get_object(self, class_name: str, object_id: str):
        return self.client.data_object.get(object_id, class_name)

    def query_objects(self, class_name: str, where: dict = None):
        return self.client.query.get(class_name, ["*"]).with_where(where).do()

    def update_object(self, class_name: str, object_id: str, updated_data: dict):
        self.client.data_object.update(updated_data, object_id, class_name)

    def delete_object(self, class_name: str, object_id: str):
        self.client.data_object.delete(object_id, class_name)