import json

import requests


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
