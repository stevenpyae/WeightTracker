import cv2
from SaveLoadCrop import SaveLoadPositions

import pytesseract
import re


def find_and_return_bfp(gaussian_blur, bfp_pattern, convert_service):
    """Apply further processing and match the pattern with the text from tesseract"""
    for i in range(3, 14):
        # Adaptive filter will run from 3 to 14
        try:
            filtered_img_for_bfp = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv2.THRESH_BINARY,
                                                         15, i)  # This is to extract body fat percentage
            # using pytesseract, get the text to match pattern
            bfp_text = convert_service.image_to_string(filtered_img_for_bfp)
            # match the pattern from the text
            matches = re.search(bfp_pattern, bfp_text)
            # match found
            if matches:
                # convert to float
                print("I found matches")
                number = float(matches.group())
                # check if number is between the range
                if 15.0 <= number <= 30.0:
                    print("Found number:", number)
                    return number
                    # break out of the loop and no need to process further
                else:
                    # Continue the loop
                    print("Number is not between 15.0 and 30.0")
                    continue
        except ValueError:
            pass


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
        # Resize the image first for cropping
        cropped_image = get_cropped_image(image, crop_positions)
        return find_and_return_bfp(cropped_image, bfp_pattern, convert_service)
    else:
        print("No crop positions found.")
        # Simulate setting crop positions
        crop_positions = SaveLoadPositions.get_crop_positions_from_image(image)
        # Save crop positions
        SaveLoadPositions.save_crop_positions(crop_positions)
        # Resize the image first for cropping
        cropped_image = get_cropped_image(image, crop_positions)
        # Process the cropped_img to extract the body fat percentage
        print("Crop positions saved:", crop_positions)

        return find_and_return_bfp(cropped_image, bfp_pattern, convert_service)


#bfp_number = get_body_fat_percentage(cv2.imread("Sample Image.jpg"))
#print(f"Body Fat Percentage: {bfp_number}")

#SaveLoadPositions.get_crop_positions_from_image(cv2.imread("Sample Image.jpg"))
