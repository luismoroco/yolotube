from typing import Any, List, Dict
import os

import cv2
import numpy as np
from google.cloud import storage
import secrets


WEIGHTS = "yolov4-tiny.weights"
CONFIG = "yolov4-tiny.cfg"
COCO_NAMES = "coco.names"
CONFIDENCE = 0.5
BUCKET_VIDEO_MINIATURE = "serverless-video-miniature"
TEMP_DIRECTORY = "tmp"
HEX_SECRETES_SIZE = 4
BASE_BUCKET_URL = "https://storage.cloud.google.com"


def get_hex_token() -> str:
    return secrets.token_hex(HEX_SECRETES_SIZE)


def get_yolo():
    net = cv2.dnn.readNet(WEIGHTS, CONFIG)

    with open(COCO_NAMES, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getUnconnectedOutLayersNames()

    return net, classes, layer_names


def process(
    cap: cv2.VideoCapture, net: Any, classes: List[str], layer_names: Any
) -> Dict:
    frame_skip = cap.get(cv2.CAP_PROP_FPS)
    current_frame = 0

    response = {}
    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

        ret, frame = cap.read()
        if not ret:
            break

        blob = cv2.dnn.blobFromImage(
            frame, 1 / 255.0, (416, 416), swapRB=True, crop=False
        )
        net.setInput(blob)

        detections = net.forward(layer_names)
        for detection in detections:
            for obj in detection:
                scores = obj[5:]
                class_id = np.argmax(scores)
                conf = scores[class_id]

                label = classes[class_id]

                if conf >= CONFIDENCE:
                    if label not in response:
                        response[label] = 1
                    else:
                        response[label] += 1

        current_frame += frame_skip

    cap.release()
    cv2.destroyAllWindows()

    return response


def get_video_and_download(event: Dict) -> str:
    file = event
    file_name = file["name"]
    bucket_name = file["bucket"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    local_file_path = f"/{TEMP_DIRECTORY}/{file_name}"
    blob.download_to_filename(local_file_path)

    return local_file_path


def get_and_save_initial_image(cap: cv2.VideoCapture, event: Dict) -> str:
    ret, frame = cap.read()
    if not ret:
        return "Error"

    file = event
    file_name = file["name"]

    miniature_name = f"{file_name}-{get_hex_token()}-miniature.jpg"
    local_file_image_initial_path = f"/{TEMP_DIRECTORY}/{miniature_name}"
    cv2.imwrite(local_file_image_initial_path, frame)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_VIDEO_MINIATURE)
    blob = bucket.blob(miniature_name)
    blob.upload_from_filename(local_file_image_initial_path)

    return miniature_name


def build_public_urls_information(event: Dict, miniature_filename: str) -> Dict:
    file = event
    video_name = file["name"]
    video_bucket_name = file["bucket"]
    return {
        "video_public_url": f"{BASE_BUCKET_URL}/{video_bucket_name}/{video_name}",
        "video_miniature_public_url": f"{BASE_BUCKET_URL}/{BUCKET_VIDEO_MINIATURE}/{miniature_filename}",
    }


def main(event, context) -> None:
    path = get_video_and_download(event=event)

    video = cv2.VideoCapture(path)
    if not video.isOpened():
        print("ERROR:", {})
    else:
        net, classes, layer_names = get_yolo()
        miniature_file = get_and_save_initial_image(cap=video, event=event)
        labels = process(cap=video, net=net, classes=classes, layer_names=layer_names)
        res = build_public_urls_information(
            event=event, miniature_filename=miniature_file
        )
        res.update(labels)

        print("OK", res)

    os.remove(path)
