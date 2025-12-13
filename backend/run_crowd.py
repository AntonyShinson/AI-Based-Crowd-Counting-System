
# run_crowd.py
import argparse
import os
import glob
import cv2
from ultralytics import YOLO
from ui import StopButtonUI

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, default="0")
parser.add_argument("--conf", type=float, default=0.25)
parser.add_argument("--model", type=str, default="yolov8n.pt")
args = parser.parse_args()

model = YOLO(args.model)
src = args.source

def is_video_path(s):
    return s.lower().endswith((".mp4", ".avi", ".mov", ".mkv", ".webm"))

is_camera = src.isdigit()
is_video = is_camera or is_video_path(src)

ui = StopButtonUI()

if is_video:
    cap = cv2.VideoCapture(int(src) if is_camera else src)
    win = "Crowd Counting"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(win, ui.mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=args.conf, max_det=1000)
        count = 0

        for r in results:
            if r.boxes is None:
                continue
            xyxy = r.boxes.xyxy.cpu().numpy()
            cls = r.boxes.cls.cpu().numpy().astype(int)
            for box, c in zip(xyxy, cls):
                if c == 0:
                    x1,y1,x2,y2 = box.astype(int)
                    cx = int((x1+x2)/2)
                    cy = y1 + int((y2-y1)*0.2)
                    cv2.circle(frame, (cx,cy), 5, (0,255,0), -1)
                    count += 1

        cv2.putText(frame, f"Count: {count}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 2)
        ui.draw_button(frame)
        cv2.imshow(win, frame)

        if cv2.waitKey(1) & 0xFF == ord("q") or ui.stop_clicked:
            break

    cap.release()
    cv2.destroyAllWindows()

else:
    frame = cv2.imread(src)
    results = model(frame, conf=args.conf, max_det=1000)
    count = 0

    for r in results:
        if r.boxes is None:
            continue
        xyxy = r.boxes.xyxy.cpu().numpy()
        cls = r.boxes.cls.cpu().numpy().astype(int)
        for box, c in zip(xyxy, cls):
            if c == 0:
                x1,y1,x2,y2 = box.astype(int)
                cx = int((x1+x2)/2)
                cy = y1 + int((y2-y1)*0.2)
                cv2.circle(frame, (cx,cy), 5, (0,255,0), -1)
                count += 1

    cv2.putText(frame, f"Count: {count}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 2)
    cv2.imshow("Crowd Counting - Image", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
