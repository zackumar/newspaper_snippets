import os
import random

import cv2
import numpy as np
from pdf2image import convert_from_path


def findBoxesInPDF(path):
    box_list = []

    newspaper_img = convert_from_path(os.path.realpath(path))
    newspaper_img[0].save('tempImage.jpg', 'JPEG')

    img = cv2.imread('tempImage.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    retval, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    invert = 255-thresh

    kernel_length = np.array(gray).shape[1]//80

    vertical_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, kernel_length))
    vertical_open = cv2.morphologyEx(
        invert, cv2.MORPH_OPEN, vertical_kernel, iterations=3)

    horizontal_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (kernel_length, 1))
    horizontal_open = cv2.morphologyEx(
        invert, cv2.MORPH_OPEN, horizontal_kernel, iterations=3)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    alpha = 0.5
    beta = 1.0 - alpha

    combined_lines_weighted = cv2.addWeighted(
        vertical_open, alpha, horizontal_open, beta, 0.0)
    combined_lines_erode = cv2.erode(
        ~combined_lines_weighted, kernel, iterations=3)
    retval, thresh1 = cv2.threshold(
        combined_lines_erode, 127, 255, cv2.THRESH_BINARY)

    combined_lines = 255-thresh1

    cv2.imwrite('./combinedLines.jpg', combined_lines)

    contours, hierarchy = cv2.findContours(
        combined_lines, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    print(contours)
    contours = contours[3:]
    print(hierarchy)

    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        if(w > 500 and h > 500):
            if(w < 2000 and h < 2000):
                box_list.append((x, y, w, h))

    cv2.imwrite('./bb_box.jpg', img)
    return box_list


def cropImage(bounding_box):
    x, y, w, h = bounding_box
    img = cv2.imread('./tempImage.jpg')
    imgH, imgW, imgC = img.shape

    centerX = x + (w // 2)
    centerY = y + (h // 2)

    x1 = x
    x2 = x + w
    y1 = y
    y2 = y + h

    x1 = centerX - 1080 // 2
    y1 = centerY - 1080 // 2
    x2 = centerX + (1080 // 2)
    y2 = centerY + (1080 // 2)

    if x1 < 0:
        x2 += -x1
        x1 += -x1

    if y1 < 0:
        y2 += -y1
        y1 += -y1

    if y2 > imgH:
        y1 -= y2 - imgH
        y2 -= y2 - imgH

    if x2 > imgW:
        x1 -= x2 - imgW
        x2 -= x2 - imgW

    cropped_img = img[y1:y2, x1:x2]

    return cropped_img


def clean():
    os.remove('tempImage.jpg')


# findSectionInPDF('./newspaper.pdf')
findImageInPDF('./newspaper.pdf')
findBoxesInPDF('./newspaper.pdf')
