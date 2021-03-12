import json

import requests
import pytesseract

import cv2


def getText(img):
    thr = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
    thresh = 255-thr

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    result = 255-close

    return pytesseract.image_to_string(result).strip()


def score(key, text, attributes=['TOXICITY']):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    tests = {}
    for attribute in attributes:
        tests[attribute] = {}

    querystring = {'key': key}
    payload_data = {'comment': {'text': text}, 'requestedAttributes': {}}
    for test in tests.keys():
        payload_data["requestedAttributes"][test] = tests[test]

    payload = json.dumps(payload_data)
    headers = {'content-type': 'application/json'}

    response = requests.post(url,
                             data=payload,
                             headers=headers,
                             params=querystring)

    return response.json()


def hasSensitiveWords(text, wordListPath):
    text = text.lower()

    with open(wordListPath) as f:
        for line in f:
            if line.rstrip() in text:
                return True
    return False
