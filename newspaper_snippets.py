import os
import random
from datetime import datetime

import cv2

import newspaper
import snippets
import ns_config
import ns_twitter

print(f'Running on {datetime.now()}...')

caption = newspaper.downloadPDF()
snippet_amount = 1

path = './newspaper.pdf'
bounding_boxes = snippets.findBoxesInPDF(path)

while len(bounding_boxes) < snippet_amount:
    caption = newspaper.downloadPDF()
    bounding_boxes = snippets.findBoxesInPDF(path)

random_box = random.choice(bounding_boxes)
cropped_img = snippets.cropImage(random_box)
cv2.imwrite('post.jpg', cropped_img)

cap_arg = caption.replace('"', '\\"')

os.popen(
    f'node ./ns_instagram.js {ns_config.instagram["username"]} {ns_config.instagram["password"]} post.jpg "{cap_arg}"').read()
print("Posted on Instagram.")

ns_twitter.postTwitter('post.jpg', caption)
print("Posted on Twitter.")

os.remove('post.jpg')

newspaper.clean()
snippets.clean()
