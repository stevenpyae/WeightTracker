import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = ('C:/Program Files/Tesseract-OCR/tesseract')

img = cv2.imread("Sample Image.jpg")
# Preprocessing the image starts

blur = cv2.GaussianBlur(img, (5,5), 0)
# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

inverted_gray = cv2.bitwise_not(gray)

'''Finding the perfect filter to get the details out of the photo'''
# Apply Histogram Equalized technique
equ = cv2.equalizeHist(inverted_gray)

# Apply Adaptive Mean thresholding
extract_date = cv2.adaptiveThreshold(inverted_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 9) #This is to extract the date
date_pattern = r"\b\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} [AP]M\b"

# Histogram Equalized
cv2.imshow('Histogram Equalized', equ)

cv2.imshow('Adaptive Gaussian', extract_date)

text = pytesseract.image_to_string(extract_date)

print(text)
matches = re.findall(date_pattern, text)

for match in matches:
    print(match)

cv2.waitKey(0)
