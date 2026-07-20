from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag


def normalize_url(url: str):
    u = urlsplit(url)

    return u.netloc + u.path


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")

    if isinstance(h1, Tag):
        return h1.get_text(strip=True)

    h2 = soup.find("h2")

    if isinstance(h2, Tag):
        return h2.get_text(strip=True)

    return ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.main

    if isinstance(main, Tag):
        main_p = main.p

        if isinstance(main_p, Tag):
            return main_p.get_text(strip=True)

    p = soup.p

    if isinstance(p, Tag):
        return p.get_text(strip=True)

    return ""


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    a = soup.find_all("a")

    result = []

    for a_tag in a:
        if isinstance(a_tag, Tag):
            href = a_tag.get("href")

            if isinstance(href, str):
                url_join = urljoin(base_url, href)
                result.append(url_join)

    return result


def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    images = soup.find_all("img")

    result = []

    for image in images:
        if isinstance(image, Tag):
            src = image.get("src")

            if isinstance(src, str):
                url_join = urljoin(base_url, src)

                result.append(url_join)

    return result
