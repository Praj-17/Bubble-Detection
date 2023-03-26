import cv2

# Load the image
img = cv2.imread(r"E:\CODING PLAYGROUND\CODE\Bubble Detection\Data\Images\image_0.jpg")

# Set the border size and color
border_size = 10
border_color = (0, 255, 0) # Green color in BGR format
img = cv2.resize(img, (1000, 600))
# Add borders to the image
img_with_border = cv2.copyMakeBorder(img, border_size, 10, 0, 400, cv2.BORDER_CONSTANT, value=border_color)

# Show the image with borders
cv2.imshow("Image with Borders", img_with_border)
cv2.waitKey(0)
cv2.destroyAllWindows()
