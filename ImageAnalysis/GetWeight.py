import re
from datetime import datetime


def get_weight_from_image(image, convert_service):
    weight_pattern = r"Weight: (\d+\.\d+)kg"

    extracted_text = convert_service.convert_to_text(image)

    matches = re.findall(weight_pattern, extracted_text)

    print(matches)
    for match in matches:
        # Check if the match is in the correct format
        if re.match(weight_pattern, match):
            return match

    return None
