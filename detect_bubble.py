#!/usr/bin/env python
# coding: utf-8


import cv2
import numpy as np

# Load the video
cap = cv2.VideoCapture('plant2.mp4')

# Loop through each frame of the video
while cap.isOpened():
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a median blur to reduce noise
    gray = cv2.medianBlur(gray, 5)

    # Apply adaptive thresholding to obtain a binary image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Define the parameters for blob detection
    params = cv2.SimpleBlobDetector_Params()
    params.filterByCircularity = True
    params.minCircularity = 0.5
    params.filterByInertia = False
    params.filterByConvexity = False
    params.filterByColor = False
    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 1000

    # Create the blob detector object and detect blobs
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(255 - thresh)

    # Loop through each blob and draw a rectangle around it
    for keypoint in keypoints:
        x, y = np.int16(keypoint.pt)
        r = np.int16(keypoint.size / 2)
        cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Bubbles detection', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

