

class TesseractService:
    import pytesseract

    def __init__(self):
        self.pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

    def convert_to_text(self, image):
        return self.pytesseract.image_to_string(image)
