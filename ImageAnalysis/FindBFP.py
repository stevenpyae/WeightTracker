import cv2
from SaveLoadCrop import SaveLoadPositions

import pytesseract
import re


def find_and_return_bfp(gaussian_blur, bfp_pattern, convert_service):
    """Apply further processing and match the pattern with the text from tesseract"""
    for i in range(3, 14):
        # Adaptive filter will run from 3 to 14
        filtered_img_for_bfp = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                     cv2.THRESH_BINARY,
                                                     15, i)  # This is to extract body fat percentage
        # using pytesseract, get the text to match pattern
        bfp_text = convert_service.image_to_string(filtered_img_for_bfp)
        # match the pattern from the text
        matches = re.search(bfp_text, bfp_pattern)
        # match found
        if matches:
            # convert to float
            number = float(matches.group())
            # check if number is between the range
            if 15.0 <= number <= 30.0:
                print("Found number:", number)
                # break out of the loop and no need to process further
                break
            else:
                # Continue the loop
                print("Number is not between 15.0 and 30.0")
                continue


def get_cropped_image(image_to_crop, crop_positions):
    """Crop the image to the size we want to extract bfp number"""
    cropped_img = image_to_crop[crop_positions[0][1]:crop_positions[1][1], crop_positions[0][0]:crop_positions[1][0]]
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0, 0, cv2.BORDER_DEFAULT)
    return gaussian_blur


# Main function
def get_body_fat_percentage(image, convert_service):
    bfp_pattern = r"\b\d+\.\d+\b"
    # Load crop positions
    crop_positions = SaveLoadPositions.load_crop_positions()

    if crop_positions:
        print("Crop positions loaded:", crop_positions)
        cropped_image = get_cropped_image(image, crop_positions)
        find_and_return_bfp(cropped_image, bfp_pattern, convert_service)
    else:
        print("No crop positions found.")
        # Simulate setting crop positions
        crop_positions = SaveLoadPositions.get_crop_positions_from_image(image)
        # Save crop positions
        SaveLoadPositions.save_crop_positions(crop_positions)

    print("Crop positions saved:", crop_positions)

    # Cut the image for processing
    # Resize the image first for cropping
    # image_resize = cv2.resize(image, resize_dimensions)
    # Cut based on Row:Row, Col:Col
    # cropped_img = image_resize[crop_positions[0][0]:crop_positions[1][0], crop_positions[0][1]:crop_positions[1][1]]

    # Process the cropped_img to extract the body fat percentage


SaveLoadPositions.get_crop_positions_from_image(cv2.imread("Sample Image.jpg"))

#
#
#
# img = cv2.imread("Sample Image.jpg")
# # Preprocessing the image starts
#
# blur = cv2.GaussianBlur(img, (5, 5), 0)
# # Convert the image to gray scale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
# gaussian_blur = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
#
# filtered_img_for_bfp = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
# 15, 9)  # This is to extract body fat percentage
#
# cv2.imshow("Image Test", filtered_img_for_bfp)
#
# bfp_text = pytesseract.image_to_string(filtered_img_for_bfp)
#
# print(bfp_text)
# cv2.waitKey(0)
