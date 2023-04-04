import cv2
import numpy as np


def far_and_close_circles(circles):
    """
    Takes a list of four circles and returns a tuple of two lists:
    - The first list contains the circle that is far from the other three
    - The second list contains the three circles that are close to each other
    """
    # Sort the circles by their y-coordinate
    sorted_circles = sorted(circles, key=lambda c: c[1])
    
    # Calculate the distance between the first circle and the other three
    distance_to_close_circles = sum(abs(sorted_circles[i][1] - sorted_circles[0][1])
                                    for i in range(1, len(circles)))
    
    # If the distance to the second circle is greater than the sum of the distances
    # to the other two circles, then the second circle is far from the other three
    if abs(sorted_circles[1][1] - sorted_circles[0][1]) > distance_to_close_circles:
        far_circle = sorted_circles[1]
        close_circles = [c for c in sorted_circles if c != far_circle]
    else:
        far_circle = sorted_circles[-1]
        close_circles = sorted_circles[:-1]
    
    return far_circle, close_circles

    
    
    

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

    edges = cv2.Canny(gray, 200, 300)


    # Detect circular arcs using Hough Transform
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 11, param1=30, param2=38, minRadius=140, maxRadius=400)


    # print(circles)
    filtered_circles = []

    # Loop over the circles
    if circles is not None:

        
        circles = np.round( circles[0, :]).astype("int")
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
        
        print(filtered_circles)
        
        far_circle, close_circles = far_and_close_circles(filtered_circles)
        
        
        for id, circle in enumerate(close_circles):
            
            color = colors[id % len(colors)]
            x,y,r = circle
            cv2.circle(image, (x, y), r, color, 2)
        return image, filtered_circles
    else:
        print('No circles Detected')
        return image, None

