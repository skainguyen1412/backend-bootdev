from urllib.parse import urlsplit
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
