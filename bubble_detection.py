
import cv2
from circle_detection import get_circles
import numpy as np
def get_bubbles(frame):
        if isinstance(frame, str):
            frame = cv2.imread(frame)
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply a median blur to reduce noise
        gray = cv2.medianBlur(gray, 5)

        # Apply adaptive thresholding to obtain a binary image
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Define the parameters for blob detection
        params = cv2.SimpleBlobDetector_Params()
        
        # params.filterByColor = True
        # params.blobColor = 220

        # Filter by area
        # Filter by area
        params.filterByArea = True
        params.minArea = 50
        params.maxArea = 1000

        # # Filter by circularity
        params.filterByCircularity = True
        params.minCircularity = 0.2

        # Filter by convexity
        params.filterByConvexity = True
        params.minConvexity = 0.3   

        # Filter by inertia ratio
        params.filterByInertia = True
        params.minInertiaRatio = 0.2

        # Create the blob detector object and detect blobs
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(255 - thresh)

        # Loop through each blob and draw a rectangle around it
        blobs = []
        for keypoint in keypoints:
            x, y = np.int16(keypoint.pt)
            r = np.int16(keypoint.size / 2)
            cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (0, 255, 0), 2)
            blobs.append((x,y,r))
        
        return frame, blobs
    

        
 

def filter_blobs(img, circles, blobs):
    # Check if each blob is within a circle
    # Set colors for visualization
    
        
    if isinstance(img, str):
        img = cv2.imread(img)
    if circles is None or blobs is None:
        return img, 0,0 
    red = (0, 0, 255)
    green = (0, 255, 0)
    false_detections = 0
    true_detections = 0
    for (x, y, r) in blobs:
        is_within_circle = False
        for (cx, cy, cr) in circles:
            if ((x-cx)**2 + (y-cy)**2) < cr**2:
                is_within_circle = True
                false_detections +=1
                break
            else:
                true_detections +=1
        if is_within_circle:
            cv2.circle(img, (x, y), r, red, 2)
        else:
            cv2.circle(img, (x, y), r, green, 2)
    return img, false_detections, true_detections

def filtered_bubbles(image):
    if isinstance(image, str):
        image = cv2.imread(image)
    
    circled_image, circles = get_circles(image)
    blob_image, blobs = get_bubbles(image)
    img, fd, td = filter_blobs(image, circles, blobs)
    return img, fd,td