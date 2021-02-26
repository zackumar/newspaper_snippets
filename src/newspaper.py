from datetime import datetime
import random
import os

import pytz
import requests

intros = [
    'Newspaper snippets',
    'Snippy snips',
    'Snippets',
    'Itty bitty pictures',
    'History',
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
    '🥰',
    '🤨',
    '👍',
    '❤️ Zack',
    'The account that gives you random newspaper pictures because why not.',
    ':)',
]

hashtags = [
    'newspaper_snippets',
    'chroniclingamerica',
    'history',
]


def downloadPDF():
    print('Downloading PDF...')
    dt = datetime.now().replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone("US/Central")).date()
    hya = dt.replace(year=dt.year - 100, day=dt.day)
    hya_pretty = hya.strftime('%B %d, %Y')

    papers_json_url = 'https://chroniclingamerica.loc.gov/frontpages/' + \
        str(hya) + '.json'

    papers_json_request = requests.get(papers_json_url)
    papers_json = papers_json_request.json()

    random_paper_json = random.choice(papers_json)
    intro = random.choice(intros)
    outro = random.choice(outros)
    publication = random_paper_json['label']
    place_of_publication = random_paper_json['place_of_publication']
    page = random.randint(1, 10)

    footer = '\n\n#' + ' #'.join(hashtags)
    caption = f'{intro} from {place_of_publication} in "{publication}", {hya_pretty}. Page {page}. - {outro} {footer}'

    print(caption)

    paper_url = random_paper_json['url'][:-2] + str(page)
    paper_pdf_url = f'https://chroniclingamerica.loc.gov/{paper_url}.pdf'

    paper_pdf_request = requests.get(paper_pdf_url)

    with open('./newspaper.pdf', 'wb') as f:
        f.write(paper_pdf_request.content)

    return caption


def clean():
    os.remove('./newspaper.pdf')