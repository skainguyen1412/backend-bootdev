from urllib.parse import urlsplit


def normalize_url(url: str):
    u = urlsplit(url)

    return u.netloc + u.path
