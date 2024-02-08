import cv2
import json
import numpy as np
import pytesseract
import re

coordinates = []
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


# Main function
def get_body_fat_percentage():
    # Load crop positions
    crop_positions = load_crop_positions()

    if crop_positions:
        print("Crop positions loaded:", crop_positions)
    else:
        print("No crop positions found.")

    # Simulate setting crop positions

    crop_positions = get_crop_positions()

    # Save crop positions
    save_crop_positions(crop_positions)
    print("Crop positions saved:", crop_positions)


def capture_mouse_clicks(event, x, y, flags, param):
    # to store coordinate and keep track of if we are cropping or not
    global coordinates, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        coordinates.append((x, y))
        cropping = False


def get_crop_positions(image_to_crop):
    global coordinates
    clone = image_to_crop.copy()

    cv2.namedWindow("image_to_crop")
    cv2.setMouseCallback("image_to_crop", capture_mouse_clicks)

    while True:
        # display image to select the coordinates
        cv2.imshow("image_to_crop", image_to_crop)
        interrupt_key = cv2.waitKey(1)

        if interrupt_key == ord("r"):
            print("Restart your inputs again")
            break

        elif interrupt_key == ord("c"):
            break

    if len(coordinates) == 2:
        print(coordinates)


get_crop_positions(cv2.imread("Sample Image.jpg"))
#
# pytesseract.pytesseract.tesseract_cmd = ('C:/Program Files/Tesseract-OCR/tesseract')
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
# filtered_img_for_bfp = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,
#                                              9)  # This is to extract body fat percentage
#
# cv2.imshow("Image Test", filtered_img_for_bfp)
#
# bfp_text = pytesseract.image_to_string(filtered_img_for_bfp)
#
# print(bfp_text)
# cv2.waitKey(0)
