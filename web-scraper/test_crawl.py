import unittest
from crawl import (
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    # Implement happy path, boundary path and error path
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute_none(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><a><span>boot.dev</span></a></body></html>"
        actual = get_urls_from_html(input_body, input_url)

        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute_multiples(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html>
            <body>
                <a href="https://crawler-test.com">
                    <span>crawler-test</span>
                </a>

                <a href="https://boot.dev">
                    <span>boot.dev</span>
                </a>

                <a href="/courses">
                    Courses
                </a>

                <a href="/lessons/python">
                    Python Lessons
                </a>

                <a href="https://example.com/about">
                    About
                </a>

                <a href="#contact">
                    Contact
                </a>
            </body>
        </html>
        """
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com",
            "https://boot.dev",
            "https://crawler-test.com/courses",
            "https://crawler-test.com/lessons/python",
            "https://example.com/about",
            "https://crawler-test.com#contact",
        ]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_to_page_url(self):
        input_url = "https://crawler-test.com/products/page.html"
        input_body = """
        <html>
            <body>
                <a href="./detail">Product detail</a>
                <a href="../about">About</a>
                <a href="/contact">Contact</a>
                <a href="?sort=asc">Sort products</a>
                <a href="#reviews">Reviews</a>
            </body>
        </html>
        """

        actual = get_urls_from_html(input_body, input_url)

        expected = [
            "https://crawler-test.com/products/detail",
            "https://crawler-test.com/about",
            "https://crawler-test.com/contact",
            "https://crawler-test.com/products/page.html?sort=asc",
            "https://crawler-test.com/products/page.html#reviews",
        ]

        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_none(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_multiples(self):
        input_url = "https://crawler-test.com/products/"
        input_body = """
        <html>
            <body>
                <img src="/logo.png" alt="Logo">

                <img src="/images/banner.jpg" alt="Banner">

                <img src="https://example.com/avatar.png" alt="Avatar">

                <img src="./assets/icon.svg" alt="Icon">

                <img src="../images/background.webp" alt="Background">

                <img src="photo.jpeg" alt="Photo">

                <img alt="Image without src">
            </body>
        </html>
        """
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/logo.png",
            "https://crawler-test.com/images/banner.jpg",
            "https://example.com/avatar.png",
            "https://crawler-test.com/products/assets/icon.svg",
            "https://crawler-test.com/images/background.webp",
            "https://crawler-test.com/products/photo.jpeg",
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
