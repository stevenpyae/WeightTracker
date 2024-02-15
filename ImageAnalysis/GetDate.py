"""This function will return the date when received an image"""

from ImageToTextService import TesseractService
import re
from datetime import datetime


def get_date_from_image(image):
    date_pattern = r"\b\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} [AP]M\b"

    convert_service = TesseractService()

    extracted_text = convert_service.convert_to_text(image)

    matches = re.findall(date_pattern, extracted_text)

    print(matches)
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
