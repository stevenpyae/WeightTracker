import cv2
import json  # Json for saving crop locations
import os  # getting .env file for resize file
from dotenv import load_dotenv  # load the env file for resizing
import pytesseract
import re

load_dotenv()
coordinates = []
cropping = False
resize_dimensions = os.environ.get('RESIZE_DIMENSIONS')
width, height = map(int, resize_dimensions.split('x'))
resize_dimensions = (width, height)

print(resize_dimensions)


def capture_mouse_clicks(event, x, y, flags, param):
    # to store coordinate and keep track of if we are cropping or not
    global coordinates, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        coordinates.append((x, y))
        cropping = False


# Function to save crop positions to a file
def save_crop_positions(positions):
    with open('crop_positions.json', 'w') as file:
        json.dump(positions, file)


# Function to retrieve crop positions from the file
def load_crop_positions():
    try:
        with open('crop_positions.json', 'r') as file:
            positions = json.load(file)
        return positions
    except FileNotFoundError:
        return None


def get_crop_positions_from_image(image_to_crop):
    global coordinates, resize_dimensions
    # instantiate the name to crop the images
    cv2.namedWindow("image_to_crop")
    cv2.setMouseCallback("image_to_crop", capture_mouse_clicks)

    # Resize the image to normalize cropping
    image_to_crop_resize = cv2.resize(image_to_crop, resize_dimensions)

    while True:
        # display image to select the coordinates
        # Resize to select coordinates
        cv2.imshow("image_to_crop", image_to_crop_resize)
        interrupt_key = cv2.waitKey(1)

        if interrupt_key == ord("r"):
            print("Restart your inputs again")
            break

        elif interrupt_key == ord("c"):
            break

    if len(coordinates) == 2:
        # Start of Test
        bfp_pattern = r"\b\d{1,2}\.\d\b"
        cropped_img = image_to_crop_resize[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0, 0, cv2.BORDER_DEFAULT)

        for i in range(3, 14):
            try:
                filtered_img_for_bfp = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                             cv2.THRESH_BINARY,
                                                             15, i)  # This is to extract body fat percentage

                print(f"Analysing Text for i = {i}")
                bfp_text = pytesseract.image_to_string(filtered_img_for_bfp)
                print(bfp_text)
                matches = re.search(bfp_pattern, bfp_text)
                if matches:
                    print('I found matches')
                    number = float(matches.group())
                    if 15.0 <= number <= 30.0:
                        print("Found number:", number)
                        break
                    else:
                        print("Number is not between 15.0 and 30.0")
            except ValueError:
                pass
        # End of test

