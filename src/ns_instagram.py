import os
import datetime
import time
import pickle
import re
import json
import random

from PIL import Image
import requests


base_url = 'https://www.instagram.com'


class Instagram:
    def __init__(self, username, password, cookie=None):
        self.credentials = {
            'username': username,
            'password': password
        }

        self.session = requests.Session()

        cookies = self.session.cookies.get_dict()
        csrftoken = cookies['csrftoken'] if 'csrftoken' in cookies else ''

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
            'Accept-Language': 'en-US',
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': base_url
        }

    def login(self):
        username = self.credentials['username']
        password = self.credentials['password']

        resp = self.session.get(f'{base_url}/', headers=self.headers)
        content = resp.text
        csrf_token = re.search('(csrf_token":")\w+', content)[0][13:]

        self.headers['X-CSRFToken'] = csrf_token

        login_form = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{self.__date()}:{password}'
        }

        resp = self.session.post(
            'https://www.instagram.com/accounts/login/ajax/', headers=self.headers, data=login_form)

        return resp.text

    def post(self, photo, caption='', post='feed'):
        isoDateObj = datetime.datetime.now().isoformat()
        now = re.sub(r'T', ' ', isoDateObj)
        now = re.sub(r'\..+', ' ', now)
        offset = round(time.timezone / 60)

    def uploadPhoto(self, photo):
        uploadId = self.__date()
        img_size = os.stat(photo).st_size
        uploadParams = {
            'media_type': '1',
            'upload_id': str(uploadId),
            'upload_media_height': '1080',
            'upload_media_width': '1080',
            'xsharing_user_ids': json.dumps([]),
            'image_compression': json.dumps({
                'lib_name': 'moz',
                'lib_version': '3.1.m',
                'quality': '80'
            }, separators=(',', ':')),
        }

        entityName = f'{uploadId}_0_{random.uniform(0, 1)}'

        photoHeaders = {
            'x-entity-type': 'image/jpeg',
            'offset': '0',
            'x-entity-name': entityName,
            'x-instagram-rupload-params': json.dumps(uploadParams, separators=(',', ':')),
            'x-entity-length': str(img_size),
            'Content-Length': str(img_size),
            'Content-Type': 'application/octet-stream',
            'x-ig-app-id': '1217981644879628',
            'Accept-Encoding': 'gzip',
            'X-Pigeon-Rawclienttime': '{:.3f}'.format(self.__date() / 1000),
            'X-IG-Connection-Speed': f'{random.uniform(0, 1)}kbps',
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0'
        }

        print(photoHeaders)

        resp = self.session.post(
            f'https://instagram.com/rupload_igphoto/{entityName}', headers=photoHeaders, data=open(photo, 'rb').read())

        return resp.text

    def __date(self):
        return int(round(time.time() * 1000))
