import requests
from bs4 import BeautifulSoup


def parse_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        soup = BeautifulSoup(response.content, 'xml')
        urls = [loc.text for loc in soup.find_all('loc')]
        return urls
    except Exception as e:
        print(f"Error - parse sitemap: {e}")
        return []


def check_not200_urls(urls):
    results = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200: # если не строго 200, то можно выставить 200 <= response.status_code <= 299
                results.append(f"{url} - {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append(f"{url} - ERROR: {str(e)}")
    return results


def save_to_file(results, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result + '\n')


def check_canonical_urls(urls):
    mismatches = []

    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                try:
                    # В некоторых ссылках были картинки
                    try:
                        parsed_xml = BeautifulSoup(response.text, 'html.parser')
                    except Exception as e:
                        parsed_xml = BeautifulSoup(response.content, 'html.parser')

                    canonical = parsed_xml.find('link', {'rel': 'canonical'})

                    if canonical:
                        try:
                            canonical_url = canonical['href'].rstrip('/')
                            original_url = url.rstrip('/')

                            if canonical_url != original_url:
                                mismatches.append(f"{original_url} - {canonical_url}")
                        except (KeyError, AttributeError):
                            mismatches.append(f"{url} - Invalid canonical tag format")
                    else:
                        mismatches.append(f"{url} - Canonical tag found")

                except Exception as e:
                    mismatches.append(f"{url} - Parser error: {str(e)}")
            else:
                mismatches.append(f"{url} - Failed, response status: {response.status_code})")

        except requests.exceptions.RequestException as e:
            mismatches.append(f"{url} - Request error: {str(e)}")

    return mismatches