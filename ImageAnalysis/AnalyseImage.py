import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = ('C:/Program Files/Tesseract-OCR/tesseract')

img = cv2.imread("Sample Image.jpg")
# Preprocessing the image starts

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

'''Finding the perfect filter to get the details out of the photo'''
# Apply Histogram Equalized technique
equ = cv2.equalizeHist(gray)

# Apply Adaptive Mean thresholding
th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)


# Histogram Equalized
cv2.imshow('Histogram Equalized', equ)

cv2.imshow('Adaptive Gaussian', th3)

text = pytesseract.image_to_string(th3)

print(text)
cv2.waitKey(0)
