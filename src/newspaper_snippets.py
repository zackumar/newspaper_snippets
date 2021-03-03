import os
import random
from datetime import datetime

import cv2

import newspaper
import snippets
import ns_instagram
import ns_twitter

import os

instagram = {
    "username": os.environ.get("instagram_username"),
    "password": os.environ.get("instagram_password"),
}

twitter = {
    "consumer_key": os.environ.get("twitter_consumer_key"),
    "consumer_secret": os.environ.get("twitter_consumer_secret"),
    "access_token_key": os.environ.get("twitter_access_token"),
    "access_token_secret": os.environ.get("twitter_access_token_secret")
}


print(f'Running on {datetime.now()}...')

print('Downloading PDF...')
caption = newspaper.downloadPDF()
print(caption)

path = './newspaper.pdf'
print('Finding rectangular contours in PDF...')

bounding_boxes = snippets.findBoxesInPDF('./newspaper.pdf')
print(f'Bounding boxes: {bounding_boxes}')
while len(bounding_boxes) == 0:
    print('Boxes empty. Downloading new...')
    caption = newspaper.downloadPDF()
    bounding_boxes = snippets.findBoxesInPDF('./newspaper.pdf')
    print(f'Bounding boxes: {bounding_boxes}')

random_box = random.choice(bounding_boxes)
print(f'Cropping image: {random_box}')
cropped_img = snippets.cropImage(random_box)
cv2.imwrite('post.jpg', cropped_img)

ns_instagram.postInstagram(instagram, 'post.jpg', caption)
print('Posted on Instagram.')

ns_twitter.postTwitter(twitter, 'post.jpg', caption)
print('Posted on Twitter.')

print('Cleaning temp files...')
os.remove('post.jpg')
newspaper.clean()
snippets.clean()
