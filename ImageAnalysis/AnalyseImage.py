import cv2

# importing Image to Text Service
from ImageToTextService import TesseractService
from GetWeight import get_weight_from_image
from GetDate import get_date_from_image
from GetBFP import get_body_fat_percentage

img = cv2.imread("Sample Image.jpg")


def analyse_image(image):
    convert_service = TesseractService()
    extracted_weight = get_weight_from_image(image, convert_service)
    extracted_date = get_date_from_image(image, convert_service)

    if extracted_date and extracted_weight:
        print("Extracted Date: ", extracted_date)
        print("Extracted Weight: ", extracted_weight)
    else:
        print("No Date")


analyse_image(img)
