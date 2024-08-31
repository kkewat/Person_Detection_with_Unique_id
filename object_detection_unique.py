# -*- coding: utf-8 -*-
"""person_detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eIoa44TRS1eYwsCVXyyiILpNdg5mWFij
"""

!pip install ultralytics opencv-python-headless

!pip install deep-sort-realtime ultralytics

from ultralytics import YOLO
import cv2
from google.colab.patches import cv2_imshow
from google.colab import files
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')  # Use 'yolov8n.pt' for faster processing

# Initialize DeepSort
tracker = DeepSort(max_age=30, n_init=3, nms_max_overlap=1.0, max_cosine_distance=0.2, nn_budget=None)

def process_video(video_path, output_path, frame_skip=5, resize_factor=0.5):
    # Open the input video
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * resize_factor)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * resize_factor)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps // frame_skip, (width, height))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Skip frames to reduce processing time
        if frame_count % frame_skip != 0:
            continue

        # Resize the frame
        frame = cv2.resize(frame, (width, height))

        # Perform detection
        results = model(frame)  # YOLOv8 detection

        # Prepare detections for DeepSort (only for persons)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                class_id = int(box.cls[0].cpu().numpy())

                if class_id == 0:  # Class 0 for 'person'
                    detections.append(([x1, y1, x2, y2], conf, class_id))

        # Update tracker with detections
        tracked_objects = tracker.update_tracks(detections, frame=frame)

        # Annotate the frame with tracking results
        for track in tracked_objects:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            bbox = track.to_tlbr().astype(int)  # Get the bounding box in (top, left, bottom, right) format
            x1, y1, x2, y2 = bbox

            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Write the annotated frame to the output video
        out.write(frame)

        # Display the frame (optional)
        cv2_imshow(frame)  # This will display the frame in Colab

    # Release the video capture and writer objects
    cap.release()
    out.release()

# Define input and output paths
input_video_path = '/content/Video1.mp4'
output_video_path = 'output_video.mp4'

# Process the video with frame skipping and resizing
process_video(input_video_path, output_video_path, frame_skip=5, resize_factor=0.5)

# Download the output video
files.download(output_video_path)