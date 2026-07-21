from urllib.parse import urlsplit
from crawl import normalize_url, extract_page_data, get_urls_from_html
import asyncio
import aiohttp


class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int, max_pages: int) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set[asyncio.Task]()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False

            if normalized_url in self.page_data:
                return False

            if len(self.page_data) > self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")

                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()

                return False

            return True

    async def get_html(self, url):
        async with self.session.get(
            url, headers={"User-Agent": "BootCrawler/1.0"}
        ) as response:
            if response.status >= 400:
                raise RuntimeError(f"Error response status code: {response.status}")

            if response.content_type != "text/html":
                raise RuntimeError("content-type is not text/html")

            html = await response.text()
            if not html:
                raise RuntimeError("Empty response value")

            return html

    async def crawl_page(self, current_url: str):
        if self.should_stop:
            return

        if not current_url:
            return

        url_split = urlsplit(current_url)

        if url_split.netloc != self.base_domain:
            return

        normalize = normalize_url(current_url)
        first_visit = await self.add_page_visit(normalize)
        if not first_visit:
            return

        async with self.semaphore:
            html = await self.get_html(current_url)

        print(f"Get html from {current_url}")
        p_d = extract_page_data(html, current_url)

        async with self.lock:
            self.page_data[normalize] = p_d

        urls = get_urls_from_html(html, current_url)

        tasks = []

        try:
            for url in urls:
                task = asyncio.create_task(self.crawl_page(url))
                tasks.append(task)
                self.all_tasks.add(task)

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            for task in tasks:
                self.all_tasks.discard(task)

    async def crawl(self):
        await self.crawl_page(self.base_url)

        return self.page_data


async def crawl_site_async(base_url: str, max_concurrency: int, max_pages: int):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        page_data = await crawler.crawl()
        return page_data
