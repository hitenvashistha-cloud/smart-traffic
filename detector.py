import os
import uuid
from collections import Counter

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}

DETECTED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "detected")
os.makedirs(DETECTED_DIR, exist_ok=True)

_model = None


def _get_model():
    global _model
    if _model is None:
        from ultralytics import YOLO
        _model = YOLO("yolov8n.pt")
    return _model


def _count_and_annotate(r):
    import cv2

    if r.boxes is None or r.boxes.cls is None:
        cls_ids = []
    else:
        cls_ids = r.boxes.cls.cpu().numpy().astype(int).tolist()

    raw_counts = Counter(cls_ids)
    vehicle_counts = {name: raw_counts.get(cid, 0) for cid, name in VEHICLE_CLASSES.items()}
    total = sum(vehicle_counts.values())

    annotated = r.plot()
    annotated_name = f"{uuid.uuid4().hex}.jpg"
    cv2.imwrite(os.path.join(DETECTED_DIR, annotated_name), annotated)

    return {
        "counts": vehicle_counts,
        "total": total,
        "annotated_filename": annotated_name,
    }


def run_detection(image_path, conf=0.25):
    model = _get_model()
    results = model(
        image_path,
        conf=conf,
        classes=list(VEHICLE_CLASSES.keys()),
        verbose=False,
    )
    return _count_and_annotate(results[0])


def run_detection_from_frame(frame, conf=0.25):
    model = _get_model()
    results = model(
        frame,
        conf=conf,
        classes=list(VEHICLE_CLASSES.keys()),
        verbose=False,
    )
    return _count_and_annotate(results[0])