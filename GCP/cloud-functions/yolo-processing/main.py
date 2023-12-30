from typing import Any, List
import os

import cv2
import numpy as np
from google.cloud import storage


WEIGHTS = "yolov4-tiny.weights"
CONFIG = "yolov4-tiny.cfg"
COCO_NAMES = "coco.names"
CONFIDENCE = 0.5


def get_yolo():
    net = cv2.dnn.readNet(WEIGHTS, CONFIG)

    with open(COCO_NAMES, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getUnconnectedOutLayersNames()

    return net, classes, layer_names


def process(
    cap: cv2.VideoCapture, net: Any, classes: List[str], layer_names: Any
) -> List[str]:
    frame_skip = cap.get(cv2.CAP_PROP_FPS)
    current_frame = 0

    response = []
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

                if label not in response and conf >= CONFIDENCE:
                    response.append(label)

        current_frame += frame_skip

    cap.release()
    cv2.destroyAllWindows()

    return response


def get_video_and_download(event) -> str:
    file = event
    file_name = file["name"]
    bucket_name = file["bucket"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    local_file_path = f"/tmp/{file_name}"
    blob.download_to_filename(local_file_path)

    return local_file_path


def main(event, context) -> None:
    path = get_video_and_download(event)

    video = cv2.VideoCapture(path)
    if not video.isOpened():
        print("ERROR:", [])
    else:
        net, classes, layer_names = get_yolo()
        res = process(cap=video, net=net, classes=classes, layer_names=layer_names)
        print("OK:", res)

    os.remove(path)
