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
inverted_gray = cv2.bitwise_not(gray)

gaussain_blur = cv2.GaussianBlur(gray, (3,3), 0, 0, cv2.BORDER_DEFAULT)

'''Finding the perfect filter to get the details out of the photo'''
# Apply Histogram Equalized technique
equalise_for_date = cv2.equalizeHist(inverted_gray)

equalise_for_weight = cv2.equalizeHist(gray)

equalise_for_bfp = cv2.equalizeHist(cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY))

# Apply Adaptive Mean thresholding
filtered_img_for_date = cv2.adaptiveThreshold(inverted_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,
                                              9)  # This is to extract the date
date_pattern = r"\b\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} [AP]M\b"
weight_pattern = r"Weight: (\d+\.\d+)kg"

filtered_img_for_weight = cv2.adaptiveThreshold(inverted_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                                15,
                                                8)  # This is to extract weight

filtered_img_for_bfp = cv2.adaptiveThreshold(gaussain_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17,
                                            9)  # This is to extract body fat percentage

# Displays

# Histogram Equalized
# cv2.imshow('Histogram Equalized', equalise_for_bfp)

# cv2.imshow('Adaptive Gaussian', filtered_img_for_bfp)
# need to de-comment start
# weight_text = pytesseract.image_to_string(filtered_img_for_weight)
#
# print(weight_text)
#
# date_text = pytesseract.image_to_string(filtered_img_for_date)
#
# matches = re.findall(date_pattern, date_text)
#
# for match in matches:
#     print(match)
#
#
# matches = re.findall(weight_pattern, weight_text)
#
# for match in matches:
#     print(match + 'kg')
# de comment end



cv2.imshow("Image Test", filtered_img_for_bfp)

bfp_text = pytesseract.image_to_string(filtered_img_for_bfp)

print(bfp_text)
cv2.waitKey(0)
