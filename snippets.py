import os
import random

import cv2
import numpy as np
from pdf2image import convert_from_path

def findBoxesInPDF(path):
	print('Finding rectangular contours in PDF...')
	box_list = []

	newspaper_img = convert_from_path(os.path.realpath(path))
	newspaper_img[0].save('tempImage.jpg', 'JPEG')

	img = cv2.imread('tempImage.jpg')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	retval, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
	invert = 255-thresh

	kernel_length = np.array(gray).shape[1]//80

	vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
	vertical_erosion = cv2.erode(invert, vertical_kernel, iterations = 3)
	vertical_dilate=cv2.dilate(vertical_erosion, vertical_kernel, iterations = 3)

	horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
	horizontal_erosion = cv2.erode(invert, horizontal_kernel, iterations = 3)
	horizontal_dilate=cv2.dilate(horizontal_erosion, horizontal_kernel, iterations = 3)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	alpha = 0.5
	beta = 1.0 - alpha

	combined_lines_weighted = cv2.addWeighted(vertical_dilate, alpha, horizontal_dilate, beta, 0.0)
	combined_lines_erode = cv2.erode(~combined_lines_weighted, kernel, iterations = 3)
	retval, thresh1 = cv2.threshold(combined_lines_erode, 127, 255, cv2.THRESH_BINARY)

	combined_lines = 255-thresh1

	contours, hierarchy = cv2.findContours(combined_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	for i in range(len(contours)):
		x,y,w,h = cv2.boundingRect(contours[i])
		# img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

		if(w > 200 and h > 200):
			# img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),4)
			box_list.append((x, y, w, h))

	# cv2.imwrite('contours.jpg', img)
	##TODO GET RID OF DRAW CODE WHEN DONEs
	
	return box_list

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
				print(f'Too close: {sample}, {(sX, sY, sW, sH)}. Resampling...')
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
	print('Cleaning temp files...')
	os.remove('tempImage.jpg')
