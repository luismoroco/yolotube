from typing import Any, List, Dict, Union
from werkzeug.utils import secure_filename
import os

from google.cloud import storage, firestore
from google.cloud.firestore_v1.base_query import FieldFilter, And, Or
from dotenv import load_dotenv

load_dotenv()

__all__ = ["GoogleStorageLoaderService", "GoogleFirestoreQueryService"]


class GoogleStorageLoaderService:
    def __init__(self) -> None:
        self.client = storage.Client()
        self.bucket_name = os.getenv("GCP_BUCKET_NAME")

    def load(self, file: Any) -> None:
        file_name = secure_filename(file.filename)
        path = os.path.join("uploads", file_name)
        file.save(path)

        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(path)


class GoogleFirestoreQueryService:
    coco_names: List[str] = [None]

    def __init__(self) -> None:
        self.client = firestore.Client(
            project=os.getenv("GCP_PROJECT_ID"),
            database=os.getenv("FIRESTORE_DATABASE_NAME"),
        )
        self.collection = self.client.collection(os.getenv("FIRESTORE_COLLECTION_NAME"))
        self.load_coco_classes()

    def load_coco_classes(self) -> None:
        with open(os.getenv("COCO_NAMES_PATH"), "r") as f:
            self.coco_names = [line.strip() for line in f.readlines()]

    def query(self, query: str = None) -> List[Dict]:
        try:
            if not query:
                # Si la query está vacía, devolver todos los documentos
                return [doc.to_dict() for doc in self.collection.get()]

            match_keys = [key for key in query.lower().split("%") if key in self.coco_names]
            query_result = self.collection.where(
                filter=FieldFilter("labels_arr", "array_contains_any", match_keys)
            ).stream()

            # Convertir los documentos a un formato de diccionario
            return [doc.to_dict() for doc in query_result]

        except Exception as e:
            # Manejar la excepción (puedes personalizar según tus necesidades)
            print(f"Error al realizar la consulta: {e}")
            return [doc.to_dict() for doc in self.collection.get()]
