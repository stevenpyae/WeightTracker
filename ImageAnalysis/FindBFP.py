import cv2
import numpy as np
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = ('C:/Program Files/Tesseract-OCR/tesseract')

img = cv2.imread("Sample Image.jpg")
# Preprocessing the image starts

blur = cv2.GaussianBlur(img, (5, 5), 0)
# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
gaussian_blur = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)


filtered_img_for_bfp = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,
                                             9)  # This is to extract body fat percentage



cv2.imshow("Image Test", filtered_img_for_bfp)

bfp_text = pytesseract.image_to_string(filtered_img_for_bfp)

print(bfp_text)
cv2.waitKey(0)
