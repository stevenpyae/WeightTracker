"""This function will return the date when received an image"""

import re
import cv2
from datetime import datetime


def filter_image_for_date(image):
    #   Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Bitwise not to Invert
    inverted_gray = cv2.bitwise_not(gray)
    filtered_img_for_date = cv2.adaptiveThreshold(inverted_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                                  15,
                                                  9)  # This is to extract the date
    return filtered_img_for_date


def get_date_from_image(image, convert_service):
    date_pattern = r"\b\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} [AP]M\b"
    # Filter Image for date & Convert to Text
    extracted_text = convert_service.convert_to_text(filter_image_for_date(image))
    # Find the matches from the extracted text
    matches = re.findall(date_pattern, extracted_text)

    # print(matches)
    for match in matches:
        # Check if the match is in the correct format
        try:
            # Attempt to parse the match as a datetime object
            parsed_date = datetime.strptime(match, "%d-%m-%Y %I:%M:%S %p")
            # If parsing succeeds, return the valid date format
            return match
        except ValueError:
            # If parsing fails, continue to the next match
            pass

    return None
