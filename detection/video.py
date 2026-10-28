import tempfile
from pathlib import Path
import cv2
import pandas as pd
from ultralytics import YOLO

def process_video(uploaded_file, confidence=0.35, max_frames=180):
    suffix = Path(uploaded_file.name).suffix or ".mp4"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        video_path = tmp.name

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("OpenCV could not open this video. Try MP4 (H.264) or AVI.")
    model = YOLO("yolov8n.pt")  # Downloads weights on first use; internet required.
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or max_frames
    stride = max(1, total // max_frames)
    rows, preview = [], None
    frame_index, analyzed = 0, 0
    while analyzed < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_index % stride == 0:
            result = model.predict(frame, conf=confidence, classes=[0], verbose=False)[0]
            count = len(result.boxes) if result.boxes is not None else 0
            annotated = result.plot()
            rows.append({"frame": frame_index, "people_count": count})
            if preview is None or count > max(r["people_count"] for r in rows[:-1] or [{"people_count": -1}]):
                preview = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            analyzed += 1
        frame_index += 1
    cap.release()
    Path(video_path).unlink(missing_ok=True)
    if not rows:
        raise ValueError("No frames could be analyzed.")
    df = pd.DataFrame(rows)
    return {
        "frames_analyzed": len(df),
        "peak_count": int(df.people_count.max()),
        "average_count": float(df.people_count.mean()),
        "preview": preview,
        "frame_counts": df
    }
