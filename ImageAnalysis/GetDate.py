"""This function will return the text while """

from ImageToTextService import TesseractService
import re


def get_date_from_image(image):
    date_pattern = r"\b\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} [AP]M\b"

    convert_service = TesseractService()

    extracted_text = convert_service.convert_to_text(image)

    matches = re.findall(date_pattern, extracted_text)

    print(matches)
    for match in matches:
        if re.match(date_pattern,match):
            return match
