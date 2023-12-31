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
        if not query:
            return [doc.to_dict() for doc in self.collection.get()]
        print("QUERY", query)
        match_keys = [key for key in query.lower().split("%") if key in self.coco_names]
        print("KEYS", match_keys)
        return [
            doc.to_dict()
            for doc in self.collection.where(
                filter=FieldFilter("labels.book", ">=", 1)
            ).stream()
        ]

    # TODO generate nested query must be fixed
    @staticmethod
    def generate_filter_constraint(keys: List[str]) -> Any:
        return And(filters=[FieldFilter(f"labels.{key}", ">=", 1) for key in keys])
