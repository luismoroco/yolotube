from typing import Any
from werkzeug.utils import secure_filename
import os

from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

__all__ = ["GoogleStorageLoaderService"]


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
