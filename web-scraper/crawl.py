from typing import TypedDict
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag
import requests


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


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


def extract_page_data(html: str, page_url: str) -> PageData:
    heading = get_heading_from_html(html)

    first_paragraph = get_first_paragraph_from_html(html)

    outgoing_links = get_urls_from_html(html, page_url)

    images_urls = get_images_from_html(html, page_url)

    return {
        "first_paragraph": first_paragraph,
        "heading": heading,
        "image_urls": images_urls,
        "outgoing_links": outgoing_links,
        "url": page_url,
    }


def get_html(url):
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

    if response.status_code >= 400:
        raise RuntimeError(f"Error response status code: {response.status_code}")

    content_type = response.headers.get("content-type", "")

    if "text/html" not in content_type.lower():
        raise RuntimeError("content-type is not text/html")

    if not response.text:
        raise RuntimeError("Empty response value")

    return response.text


def crawl_page(base_url, current_url: str, page_data: dict[str, PageData]):
    if not current_url:
        return

    url_split = urlsplit(current_url)
    base_url_split = urlsplit(base_url)

    if url_split.netloc != base_url_split.netloc:
        return

    normalize = normalize_url(current_url)

    if normalize in page_data:
        return

    html = get_html(current_url)
    print(f"Get html from {current_url}")
    p_d = extract_page_data(html, current_url)
    page_data[normalize] = p_d
    urls = get_urls_from_html(html, current_url)

    for url in urls:
        crawl_page(base_url, url, page_data)
