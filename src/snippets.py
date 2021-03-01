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

        combined_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(contours)
    contours = contours[3:]
    print(hierarchy)

    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
        if(w > 200 and h > 200):
            box_list.append((x, y, w, h))

    cv2.imwrite('./bb_box.jpg', img)
    return box_list


def findSectionInPDF(path):
    # newspaper_img = convert_from_path(os.path.realpath(path))
    # newspaper_img[0].save('tempImage.jpg', 'JPEG')

    img = cv2.imread('tempImage.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, inv_thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    line_img = gray.copy() * 0

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    remove_horizontal = cv2.morphologyEx(
        inv_thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=3)
    cnts = cv2.findContours(
        remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(line_img, [c], -1, (255, 255, 255), 5)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    remove_vertical = cv2.morphologyEx(
        inv_thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=3)
    cnts = cv2.findContours(
        remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(line_img, [c], -1, (255, 255, 255), 5)

    clean = cv2.subtract(inv_thresh, line_img)

    dilation_type = cv2.MORPH_RECT
    horizontal_dilation = 10
    vertical_dilation = 1
    element = cv2.getStructuringElement(
        dilation_type, (2*horizontal_dilation + 1, 2*vertical_dilation+1), (horizontal_dilation, vertical_dilation))
    dilation_thresh = cv2.dilate(clean, element)

    filled_thresh = dilation_thresh.copy()
    contours, hierarchy = cv2.findContours(
        dilation_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        cv2.drawContours(filled_thresh, [cnt], -1, 255, cv2.FILLED)

    cv2.imwrite('filled.jpg', filled_thresh)


def findImageInPDF(path):
    img = cv2.imread('tempImage.jpg')
    imgH, imgW, imgC = img.shape
    original = img.copy()
    blank = np.zeros(img.shape[:2], dtype=np.uint8)
    inv_gray = 255-cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(inv_gray, (5, 5), 0)
    cv2.imwrite('./blur.jpg', blur)
    retval, thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imwrite('./thresh.jpg', thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
    cv2.imwrite('./close1.jpg', close)

    cnts = cv2.findContours(close, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(original, (x, y), (x+w, y+h), (0, 0, 255), 3)

    cv2.imwrite('./bb.jpg', original)


def getRandomBoxes(box_list, n, nearness):
    print('Getting random samples...')
    random_samples = []
    while len(random_samples) != n:
        cont = False
        sample = random.choice(box_list)
        if sample in random_samples:
            print(f'Repeat {sample}. Resampling...')
            continue
        for sX, sY, sW, sH in random_samples:
            (x, y, w, h) = sample
            if abs(sX - x) < nearness and abs(sY - y) < nearness:
                print(
                    f'Too close: {sample}, {(sX, sY, sW, sH)}. Resampling...')
                cont = True
                break
        if cont:
            continue

        random_samples.append(sample)

    print('Samples: ' + str(random_samples))
    return random_samples


def cropImage(bounding_box):
    print(f'Cropping image: {bounding_box}')

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
