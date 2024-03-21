import re
import cv2


def filter_image_for_weight(image):
    #   Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_gray = cv2.bitwise_not(gray)
    filtered_img_for_weight = cv2.adaptiveThreshold(inverted_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                    cv2.THRESH_BINARY,
                                                    15,
                                                    8)  # This is to extract weight
    return filtered_img_for_weight


def get_weight_from_image(image, convert_service):
    weight_pattern = r"Weight: (\d+\.\d+)kg"

    extracted_text = convert_service.convert_to_text(filter_image_for_weight(image))

    matches = re.findall(weight_pattern, extracted_text)
    print(matches)
    # if weight pattern is found, return as float
    try:
        if matches:
            # get the first match where weight is extracted
            number = float(matches[0])
            if 60.0 <= number <= 70.0:
                print("Found number:", number)
                return number
                # break out of the loop and no need to process further
            else:
                # Continue the loop
                print("Invalid Weight")
    except ValueError:
        return None
