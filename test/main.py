from ultralytics import YOLO
import cv2
import cvzone
import math
import sys

model = YOLO("yolov5s.pt")

classNames = [
    "person",
    "bicycle",
    "car",
    "motorbike",
    "aeroplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "sofa",
    "pottedplant",
    "bed",
    "diningtable",
    "toilet",
    "tvmonitor",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]

res = {}


def main(cap: cv2.VideoCapture) -> None:
    frame_skip = cap.get(cv2.CAP_PROP_FPS)
    current_frame = 0

    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(frame, (x1, y1, w, h))

                conf = math.ceil((box.conf[0] * 100)) / 100

                cls = box.cls[0]
                name = classNames[int(cls)]

                if conf >= 0.5:
                    if name not in res:
                        res[name] = 1
                    else:
                        res[name] += 1

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        current_frame += frame_skip

    cap.release()
    cv2.destroyAllWindows()


def get_and_save_initial_image(cap: cv2.VideoCapture) -> None:
    ret, frame = cap.read()
    if not ret:
        return

    local_file_image_initial_path = "frame1.jpg"
    cv2.imwrite(local_file_image_initial_path, frame)


if __name__ == "__main__":
    iFile = cv2.VideoCapture("../data/video/NY-lite.mp4")

    if not iFile.isOpened():
        sys.exit()

    get_and_save_initial_image(iFile)
    main(iFile)
    print("Response: ", res)
