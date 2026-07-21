import asyncio
import sys

from async_crawler import crawl_site_async


async def main_async():
    print("Hello from web-scraper!")

    argument_len = len(sys.argv)

    if argument_len < 2:
        print("no website provided")
        sys.exit(1)

    if argument_len > 2:
        print("too many arguments provided")
        sys.exit(1)

    BASE_URL = sys.argv[1]
    print(f"starting crawl of: {BASE_URL}")

    page_data = await crawl_site_async(BASE_URL, 5)

    for data in page_data.values():
        print(data)


if __name__ == "__main__":
    asyncio.run(main_async())
