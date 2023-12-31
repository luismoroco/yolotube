import os
import sys

from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

from service import GoogleStorageLoaderService


load_dotenv()


__all__ = ["app"]


app = Flask(__name__)

GCP_CREDENTIAL_PATH = os.getenv("GCP_CREDENTIAL_PATH")
GCP_CREDENTIAL_FILENAME = os.getenv("GCP_CREDENTIAL_FILENAME")

if not GCP_CREDENTIAL_PATH or not GCP_CREDENTIAL_FILENAME:
    sys.exit()

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = f"{GCP_CREDENTIAL_PATH}/{GCP_CREDENTIAL_FILENAME}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file_to_bucket():
    file = request.files["archivo"]

    try:
        GoogleStorageLoaderService().load(file=file)
        return jsonify({"message": "OK"}), 200
    except Exception as e:
        return render_template("error.html", error=e), 500
