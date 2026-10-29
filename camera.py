import urllib.request

import cv2
import numpy as np


def grab_frame(url, timeout=5):
    if not url:
        return None
    url = url.strip()

    # Try as a single JPEG (works for IP Webcam /shot.jpg and any image URL)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        arr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is not None:
            return frame
    except Exception:
        pass

    # Fallback: OpenCV VideoCapture (MJPEG / RTSP)
    try:
        cap = cv2.VideoCapture(url)
        if cap.isOpened():
            ok, frame = cap.read()
            cap.release()
            if ok:
                return frame
    except Exception:
        pass

    return None