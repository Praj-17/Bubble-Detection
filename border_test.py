import cv2



image = cv2.imread("Data\Images\image_20.jpg")
image = cv2.copyMakeBorder(image, 80, 0,0,0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
cv2.imshow("image", image)
cv2.waitKey(0)