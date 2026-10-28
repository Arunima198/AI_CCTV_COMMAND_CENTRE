# AI-CCTV Command Center — from-scratch starter

## Features
- Synthetic crowd dataset generator (no camera required)
- CSV upload and validation (`people_count` required; `timestamp` and `zone` optional)
- Threshold-based zone summaries and alert table
- Optional uploaded-video analysis using YOLOv8 person class
- Crowd Management and Tourism / Heritage summaries

## Windows setup
Open CMD in this project folder, then run:

```bat
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the Local URL printed in the terminal, usually http://localhost:8501.

## Demo without a camera
Choose **Synthetic dataset** in the sidebar. It generates simulated records and shows counts, charts, zone summaries, and threshold alerts.

## Use a Kaggle dataset
Download a CSV from Kaggle. It must contain a numeric `people_count` column. If it uses other column names, rename the relevant column to `people_count`; optionally provide `timestamp` and `zone`. Upload it using **Upload CSV**.

A dataset of images/video is not the same as a tabular count dataset. For YOLO visual detections, use **Upload video**.

## Video mode
Upload MP4/AVI/MOV/MKV and click **Analyze uploaded video**. The first use downloads `yolov8n.pt`, requiring internet. CPU processing can be slow.
The displayed count is per sampled frame, not unique people or true entry/exit footfall.

## Folder structure
```
ai_cctv_from_scratch/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── detection/
│   ├── __init__.py
│   ├── analytics.py
│   └── video.py
└── modes/
    ├── __init__.py
    ├── crowd.py
    └── tourism.py
```

## Limitations
- Synthetic data is simulated.
- CSV charts summarize the supplied records; they do not run object detection.
- Video counts can be affected by occlusion, camera angle, frame sampling, and model errors.
- Queue wait time, identity tracking, and real CCTV/RTSP integration are not implemented.
