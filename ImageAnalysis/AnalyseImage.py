import cv2

# importing Image to Text Service
from ImageToTextService import TesseractService
from GetWeight import get_weight_from_image
from GetDate import get_date_from_image
from GetBFP import get_body_fat_percentage

img = cv2.imread("Sample Image.jpg")
# Preprocessing the image starts

blur = cv2.GaussianBlur(img, (5, 5), 0)
# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
inverted_gray = cv2.bitwise_not(gray)

'''Finding the perfect filter to get the details out of the photo'''
# Apply Histogram Equalized technique
equalise_for_date = cv2.equalizeHist(inverted_gray)

equalise_for_weight = cv2.equalizeHist(gray)

# Apply Adaptive Mean thresholding
filtered_img_for_date = cv2.adaptiveThreshold(inverted_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,
                                              9)  # This is to extract the date

filtered_img_for_weight = cv2.adaptiveThreshold(inverted_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                                15,
                                                8)  # This is to extract weight


def analyse_image(image):
    convert_service = TesseractService()
    extracted_date = get_weight_from_image(image, convert_service)

    if extracted_date:
        print(extracted_date)
    else:
        print("No Date")


analyse_image(img)
