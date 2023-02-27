
# In[1]:


import cv2
import numpy as np

def get_circles(image, lower_bound = [141,141,121], upper_bound=[150,150,220]):
    """Function Takes in an image both as an array or as a path, Masks it with Red color and returns the detected circles"""
    if isinstance(image, str):
        image = cv2.imread(image)
    
    def mask_color(img, lower_bound:list, upper_bound:list):
        lower_bound = np.array(lower_bound, dtype = "uint8") 
        upper_bound = np.array(upper_bound, dtype = "uint8")
        mask = cv2.inRange(img, lower_bound, upper_bound)
        return cv2.bitwise_and(img, img, mask =  mask) 
    
    # Convert the image to grayscale
    img = mask_color(image, [121,121,121], [150,150,220])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to smooth the image and reduce noise
    gray = cv2.GaussianBlur(gray, (9,9), 2, 2)

    # Apply HoughCircles with varying parameters to detect circles of different sizes
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=15, minRadius=100, maxRadius=500)

    filtered_circles = []

    # Loop over the circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Initialize a flag to indicate whether the circle has been filtered
            filtered = False

            # Loop over the filtered circles
            for (fx, fy, fr) in filtered_circles:
                # Calculate the distance between the centers of the circles
                d = np.sqrt((x - fx)**2 + (y - fy)**2)

                # If the distance is smaller than the sum of their radii, remove the circle with the smaller radius
                if d < r + fr:
                    filtered = True
                    if r < fr:
                        break

            # If the circle was not filtered, add it to the list of filtered circles
            if not filtered:
                filtered_circles.append((x, y, r))

        colors = [(0, 255, 255), (255, 0, 255),(255, 0, 0), (255, 255, 0), (0, 0, 255)]

        for id, circle in enumerate(filtered_circles):
            color = colors[id % len(colors)]
            x, y, r = circle
            cv2.circle(image, (x, y), r, color, 2)

        return image, filtered_circles
    else:
        print('No circles Detected')
        return image, None


# In[2]:


cap = cv2.VideoCapture('data/plant.mp4')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (int(cap.get(3)),int(cap.get(4))))

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:
        # Apply the circle detection function to the frame
        output_frame, _ = get_circles(frame)

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


# In[ ]:




