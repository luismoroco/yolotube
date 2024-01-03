import os
import sys

from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from service import GoogleStorageLoaderService, GoogleFirestoreQueryService


load_dotenv()


__all__ = ["app"]


app = Flask(__name__, static_url_path='/static')
CORS(app)

GCP_CREDENTIAL_PATH = os.getenv("GCP_CREDENTIAL_PATH")
GCP_CREDENTIAL_FILENAME = os.getenv("GCP_CREDENTIAL_FILENAME")

if not GCP_CREDENTIAL_PATH or not GCP_CREDENTIAL_FILENAME:
    sys.exit()

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = f"{GCP_CREDENTIAL_PATH}/{GCP_CREDENTIAL_FILENAME}"

query_eng = GoogleFirestoreQueryService()


@app.route("/")
def index():
    return render_template("index.html", message="Sube tu video aquí")


@app.route("/upload", methods=["POST"])
def upload_file_to_bucket():
    file = request.files["archivo"]
    print(file)
    try:
        GoogleStorageLoaderService().load(file=file)
        return render_template("index.html", message="¡Video Guardado en Bucket!"), 200
    except Exception as e:
        return render_template("error.html", error=e), 500


@app.route("/data/", methods=["GET"])
def list_items():
    query = request.args.get("query", None)

    try:
        data = query_eng.query(query=query)
        return jsonify({"message": "OK", "data": data}), 200
    except Exception as e:
        return jsonify({"message": e, "data": []}), 500
