import pytest
import requests


base_url = '' + 'robots.txt'  # Сайт формата https://site.site/


@pytest.fixture()
def get_sitemap_url():
    """
    Фикстура подготовки, GET запрос к сайту, что бы получить данные из robots.txt
    :return: str
    """
    try:
        response = requests.get(base_url)
        for line in response.text.split('\n'):
            if line.lower().startswith('sitemap'):
                return line.split(':', 1)[1].strip()
    except Exception as e:
        print(f'Cant get sitemap: {e}')
