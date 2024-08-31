# Person_Detection_with_Unique_id
# Person Detection and Tracking with YOLOv8 and DeepSort

## Overview
This project implements a person detection and tracking system using YOLOv8 for object detection and DeepSort for tracking. The goal is to detect and track persons in a video, assigning unique IDs to each detected person, and handle scenarios where individuals re-enter the frame or are partially occluded.

## Features
- **Person Detection**: Uses YOLOv8 to detect persons in video frames.
- **Tracking**: Employs DeepSort to track detected persons across frames, even through occlusions and re-entries.
- **Output**: Produces a video with bounding boxes and unique IDs overlaid on the detected persons.

## Setup Instructions

### Prerequisites
Ensure you have Python 3.7+ installed. This project uses Google Colab, so no local setup is required if you are using Colab.

### Installing Dependencies
You need to install the following Python packages:
- `ultralytics` for YOLOv8
- `deep-sort-realtime` for tracking
- `opencv-python-headless` for video processing

You can install these dependencies using the following commands:

```bash
pip install ultralytics deep-sort-realtime opencv-python-headless
