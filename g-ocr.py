import pytesseract
from PIL import Image


"""
谷歌ocr引擎
brew install tesseract 

百度ocr引擎
pip install "paddleocr>=2.0.1"

"""

def ocr_recognition(image_filename):
    # Open the image file
    img = Image.open(image_filename)
    
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img)

    return text

# Test the function
image_filename = './0000520708.jpg'  # replace with your image file name
print(ocr_recognition(image_filename))

