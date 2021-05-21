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

print('Downloading JP2...')
img, insta_caption, twit_caption = newspaper.downloadJP2()

print('Finding rectangular contours in JP2...')

bounding_boxes = snippets.findBoxes(img)
print(f'Bounding boxes: {bounding_boxes}')
while len(bounding_boxes) == 0:
    print('No valid bounding boxes. Downloading new PDF...')
    img, insta_caption, twit_caption = newspaper.downloadJP2()
    bounding_boxes = snippets.findBoxes(img)
    print(f'Bounding boxes: {bounding_boxes}')

print(f'Caption: {insta_caption}')

random_box = random.choice(bounding_boxes)
print(f'Cropping image: {random_box}')
cropped_img = snippets.cropImage(img, random_box)
cv2.imwrite('post.jpg', cropped_img)

print('Starting instagram post')
ns_instagram.postInstagram(instagram, 'post.jpg', insta_caption)
print('Posted on Instagram.')

print('Starting twitter post')
ns_twitter.postTwitter(twitter, 'post.jpg', twit_caption)
print('Posted on Twitter.')

print('Cleaning temp files...')
os.remove('post.jpg')
