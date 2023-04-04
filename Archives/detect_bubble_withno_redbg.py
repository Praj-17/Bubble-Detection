

# In[2]:


def is_red_around(frame, x, y, radius):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color ranges for red and yellow
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    
    # Get the pixels surrounding the bubble
    x1, y1 = max(0, x - radius), max(0, y - radius)
    x2, y2 = min(frame.shape[1] - 1, x + radius), min(frame.shape[0] - 1, y + radius)
    bubble_pixels = hsv[y1:y2, x1:x2, :]
    
    # Check if the pixels are either red or yellow
    red_mask = cv2.inRange(bubble_pixels, lower_red, upper_red)
    yellow_mask = cv2.inRange(bubble_pixels, lower_yellow, upper_yellow)
    surrounded_by_red = np.sum(red_mask) > 0
    surrounded_by_yellow = np.sum(yellow_mask) > 0
    
    # If the bubble is not surrounded by red or yellow, draw a green circle around it
    if not surrounded_by_red or not surrounded_by_yellow:
        return False
    else:
        return True


# In[6]:


import numpy as np

def is_red_around(img, x, y, radius, threshold):
    """
    Checks if the coordinates of a bubble in the given image are surrounded by red or yellow color from at least two sides.

    Parameters:
    - img: numpy array, the image where the bubble was detected
    - center: tuple (x,y), the coordinates of the center of the bubble
    - radius: int, the radius of the bubble
    - red_lower: numpy array, the lower bounds of the red color range
    - red_upper: numpy array, the upper bounds of the red color range
    - yellow_lower: numpy array, the lower bounds of the yellow color range
    - yellow_upper: numpy array, the upper bounds of the yellow color range
    - threshold: int, the threshold for the sum of pixel values in the binary mask

    Returns:
    - True if the bubble is surrounded by red or yellow color from at least two sides, False otherwise
    """
    # Define color ranges for red and yellow
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    
    # create a binary mask of the same size as the image
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    # set the regions with red or yellow colors to 1 in the binary mask
    red_mask = cv2.inRange(img, red_lower, red_upper)
    yellow_mask = cv2.inRange(img, yellow_lower, yellow_upper)
    mask[(red_mask > 0) | (yellow_mask > 0)] = 1

    # compute the sum of pixel values within a certain radius around the center of the bubble in the binary mask
    
    x_min = max(x - radius, 0)
    x_max = min(x + radius, img.shape[1] - 1)
    y_min = max(y - radius, 0)
    y_max = min(y + radius, img.shape[0] - 1)
    sum_values = np.sum(mask[y_min:y_max, x_min:x_max])
    
    if sum_values >= threshold:
        return True
    else:
        return False

    # return True if the sum of pixel values is greater than the threshold, False otherwise
    #return sum_values >= threshold


# In[88]:


import numpy as np
import cv2

def is_red_around(image, x, y, threshold):
    # Get dimensions of image
    height, width, _ = image.shape
    
    # Get RGB color of center pixel
    center_color = image[y, x]
    
    # Check if center pixel is red or yellow
    if center_color[0] >= threshold or center_color[1] >= threshold:
        return False
    
    # Look for red or yellow color in surrounding pixels
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Skip the center pixel
            if i == j == 0:
                continue
            
            # Calculate coordinates of current pixel
            current_x, current_y = x + i, y + j
            
            # Skip pixels outside the image boundaries
            if current_x < 0 or current_x >= width or current_y < 0 or current_y >= height:
                continue
            
            # Get RGB color of current pixel
            current_color = image[current_y, current_x]
            
            # Check if current pixel is red or yellow
            if current_color[0] >= threshold or current_color[1] >= threshold:
                return True
    
    return False


# In[13]:


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
    params.filterByCircularity = True
    params.minCircularity = 0.1
    params.filterByInertia = True
    params.minInertiaRatio = 0.3
    params.filterByConvexity = True
    params.minConvexity = 0.3
    params.filterByColor = False
    params.filterByArea = True
    params.minArea = 150
    params.maxArea = 1000

    # Create the blob detector object and detect blobs
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(255 - thresh)

    # Loop through each blob and draw a rectangle around it
    for keypoint in keypoints:
        x, y = np.int16(keypoint.pt)
        r = np.int16(keypoint.size / 2)
        cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (0, 255, 0), 2)

        # Loop through each blob and draw a rectangle around it
        blobs = []
        for keypoint in keypoints:
            x, y = np.int16(keypoint.pt)
            r = np.int16(keypoint.size / 2)
             #Check if the blob is surrounded by red or yellow
            if is_red_around(frame, x, y, r+1, 1000):
                continue
                cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (0, 255, 0), 2)
            blobs.append((x,y,r))
        
        return frame, blobs


# In[16]:


import numpy as np
import cv2
cap = cv2.VideoCapture('Data/plant.mp4')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (int(cap.get(3)),int(cap.get(4))))

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:
        # Apply the circle detection function to the frame
        output_frame, _ = get_bubbles(frame)

        # Write the frame into the video
        out.write(output_frame)

        # Display the resulting frame
        cv2.imshow('frame',output_frame)

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

