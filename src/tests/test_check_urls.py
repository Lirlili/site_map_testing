from src.helpers.base_helpers import (
    parse_sitemap,
    check_not200_urls,
    save_to_file,
    check_canonical_urls,
)


def test_check(get_sitemap_url):
    all_urls = parse_sitemap(get_sitemap_url)
    bad_urls = check_not200_urls(all_urls)
    if bad_urls:
        save_to_file(bad_urls, 'bad_urls.txt')
    assert not bad_urls


def test_canonical(get_sitemap_url):
    all_urls = parse_sitemap(get_sitemap_url)
    not_canonincal = check_canonical_urls(all_urls)
    if not_canonincal:
        save_to_file(not_canonincal, 'not_canonical.txt')
    assert not not_canonincal
