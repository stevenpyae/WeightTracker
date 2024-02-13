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
        print(coordinates)
        cropped_img = image_to_crop_resize[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0, 0, cv2.BORDER_DEFAULT)

        for i in range(8, 14):
            filtered_img_for_bfp = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv2.THRESH_BINARY,
                                                         15, i)  # This is to extract body fat percentage

            print(f"Analysing Text for i = {i}")
            bfp_text = pytesseract.image_to_string(filtered_img_for_bfp)
            print(bfp_text)

        cv2.waitKey(0)
        return coordinates


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


# Main function
def get_body_fat_percentage(image):
    global resize_dimensions
    # Load crop positions
    crop_positions = load_crop_positions()

    if crop_positions:
        print("Crop positions loaded:", crop_positions)
    else:
        print("No crop positions found.")
        # Simulate setting crop positions
        crop_positions = get_crop_positions_from_image(image)
        # Save crop positions
        save_crop_positions(crop_positions)

    print("Crop positions saved:", crop_positions)

    # Cut the image for processing
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
    # Resize the image first for cropping
    image_resize = cv2.resize(image, resize_dimensions)
    # Cut based on Row:Row, Col:Col
    cropped_img = image_resize[crop_positions[0][0]:crop_positions[1][0], crop_positions[0][1]:crop_positions[1][1]]

    # Process the cropped_img to extract the body fat percentage


get_crop_positions_from_image(cv2.imread("Sample Image.jpg"))

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
