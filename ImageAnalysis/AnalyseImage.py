import cv2

img = cv2.imread("Sample Image.jpg")

cv2.imshow("Image", img)
cv2.waitKey(0)