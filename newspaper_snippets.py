import os
import random
from datetime import datetime

import cv2

import newspaper
import snippets

print(f'Running on {datetime.now()}...')

caption = newspaper.downloadPDF()
snippet_amount = 1

path = './newspaper.pdf'
bounding_boxes = snippets.findBoxesInPDF(path)

while len(bounding_boxes) < snippet_amount:
	caption =  newspaper.downloadPDF()
	bounding_boxes = snippets.findBoxesInPDF(path)

random_box = random.choice(bounding_boxes)
cropped_img = snippets.cropImage(random_box)
cv2.imwrite('post.jpg', cropped_img)

cap_arg = caption.replace('"', '\\"')

os.popen(f'node ./instagram.js post.jpg "{cap_arg}"').read()
print("Posted.")

os.remove('post.jpg')

newspaper.clean()
snippets.clean()