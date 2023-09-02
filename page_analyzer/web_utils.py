import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from validators.url import url as is_correct_url


def validate_url(url: str):
    errors = []
    if len(url) > 255:
        error = 'URL превышает 255 символов'
        errors.append(error)
    elif not url:
        error = 'URL обязателен для ввода'
        errors.append(error)
    elif not is_correct_url(url):
        error = 'URL не прошел валидацию'
        errors.append(error)


def get_normalyze_url(url: str) -> str:
    parsed_url = urlparse(url)
    normalyze_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return normalyze_url


def get_status_code_by_url(url: str) -> int:
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException:
        return 0


def get_tags_data(url_name):
    h1 = ''
    title = ''
    description = ''

    resp = requests.get(url_name)
    soup = BeautifulSoup(resp.text, 'html.parser')

    h1 = soup.h1.text if soup.h1 else h1
    title = soup.title.text if soup.title else title
    meta_tag = soup.find('meta', attrs={'name': 'description'})

    if meta_tag:
        description = meta_tag.get('content')

    return {
        'h1': h1,
        'title': title,
        'description': description,
    }
