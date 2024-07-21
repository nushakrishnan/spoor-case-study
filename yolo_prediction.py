# Ref: https://docs.ultralytics.com/usage/python/#predict

import os
import cv2
from PIL import Image
from ultralytics import YOLO
from datetime import timedelta
import pandas as pd

home = os.path.expanduser('~')
image_dir = f"{home}/Documents/assignments/spoor/images/"
model_dir = f"{home}/Documents/assignments/spoor/yolov8n.pt"
model = YOLO(model=model_dir)
image_files = sorted(os.listdir(image_dir))
image_files = [
    os.path.join(image_dir, image_file) for image_file in image_files
    if image_file.endswith('.png')
]

csv_file = './data/predictions.csv'
video_file = './data/pigeon.mp4'
video = cv2.VideoCapture(video_file)
if not video.isOpened():
    raise Exception('Error opening video file')

fps = video.get(cv2.CAP_PROP_FPS)
csv_results = []

for image_file in image_files:
    frame = Image.open(image_file)
    frame_index = int(os.path.basename(image_file).split('_')[1].split('.')[0])
    results = model(frame)

    timestamp_seconds = frame_index / fps
    timestamp = str(timedelta(seconds=timestamp_seconds)).split('.')[0]

    for result in results:
        for detection in result.boxes:
            x1, y1, x2, y2 = map(float, detection.xywhn[0])
            label = model.names[int(detection.cls[0])]
            confidence = float(detection.conf[0])

            csv_results.append({
                'Class': label,
                'Timestamp': timestamp,
                'Frame': frame_index,
                'BoundingBox_Coord_1': x1,
                'BoundingBox_Coord_2': y1,
                'BoundingBox_Coord_3': x2,
                'BoundingBox_Coord_4': y2,
                'Confidence': confidence
            })

video.release()
data = pd.DataFrame(csv_results)
data.to_csv(csv_file, index=False)
print(f"Predictions saved to {csv_file}")
