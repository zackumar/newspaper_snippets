import pytesseract
from PIL import Image
import cv2


def isSensitive(img, word_list):
    ocr = pytesseract.image_to_string(img).lower()

    with open(word_list) as f:
        for word in f:
            if word.lower().strip() in ocr:
                return True

    return False


print(isSensitive(cv2.imread('./post.jpg'), './sensitivewords.txt'))
