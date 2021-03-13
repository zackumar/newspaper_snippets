from datetime import datetime
import random
import os

import pytz
import requests
import cv2
import numpy as np

intros = [
    'Newspaper snippets',
    'Snippy snips',
    'Snippets',
    'Itty bitty pictures',
    'Clips',
    'Clippets',
    'Snip snaps',
    'Snip snips',
    'Whatever they\'re called',
    'Snippies',
    'Random knick-knacks',
    'Thingy things',
]

outros = [
    ':D',
    ':P',
    '<3',
    'newspaper_snippets ❤️',
    '❤️',
    '✨',
    '😊',
    '😃',
    '😛',
    '🥰',
    '🤨',
    '👍',
    'Zack ❤️',
    'The account that gives you random newspaper pictures because why not?',
    ':)',
]

warning = '\n\nHello. Zack here. Because these are snapshots of history, some are bound to be offensive. If you believe this post is overly offensive, feel free to DM me. - Z.U.'

hashtags = [
    'newspaper_snippets',
    'chroniclingamerica',
    'history',
]


def downloadJP2():
    dt = datetime.now().replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone("US/Central")).date()
    hya = dt.replace(year=dt.year - 100, day=dt.day)
    hya_pretty = hya.strftime('%B %d, %Y')

    papers_json_url = 'https://chroniclingamerica.loc.gov/frontpages/' + \
        str(hya) + '.json'

    papers_json_resp = requests.get(papers_json_url)
    papers_json = papers_json_resp.json()

    random_paper_json = random.choice(papers_json)
    intro = random.choice(intros)
    outro = random.choice(outros)
    publication = random_paper_json['label']
    place_of_publication = random_paper_json['place_of_publication']
    page = random.randint(1, random_paper_json['pages'])

    footer = '\n\n#' + ' #'.join(hashtags)
    insta_caption = f'{intro} from {place_of_publication} in "{publication}", {hya_pretty}. Page {page}. - {outro} {warning} {footer}'
    twit_caption = f'{intro} from {place_of_publication} in "{publication}", {hya_pretty}. Page {page}. - {outro} {footer}'

    paper_url = random_paper_json['url'][1:-2] + str(page)
    paper_pdf_url = f'https://chroniclingamerica.loc.gov/{paper_url}.jp2'

    paper_pdf_resp = requests.get(paper_pdf_url, stream=True).raw
    img = np.asarray(bytearray(paper_pdf_resp.read()), dtype="uint8")
    image = cv2.imdecode(img, cv2.IMREAD_COLOR)

    return (image, insta_caption, twit_caption)
