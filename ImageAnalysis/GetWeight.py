import re


def get_weight_from_image(image, convert_service):
    weight_pattern = r"Weight: (\d+\.\d+)kg"

    extracted_text = convert_service.convert_to_text(image)

    matches = re.findall(weight_pattern, extracted_text)
    print(matches)
    # if weight pattern is found, return as float
    try:
        if matches:
            #get the first match where weight is extracted
            number = float(matches[0])
            if 60.0 <= number <= 70.0:
                print("Found number:", number)
                return number
                # break out of the loop and no need to process further
            else:
                # Continue the loop
                print("Number is not between 15.0 and 30.0")
    except ValueError:
        return None
