import unittest
from crawl import (
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data,
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

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_empty_html(self):
        input_url = "https://crawler-test.com/page"

        actual = extract_page_data("", input_url)

        expected = {
            "url": input_url,
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_multiple_urls_and_missing_attributes(self):
        input_url = "https://crawler-test.com/products/page.html"
        input_body = """
        <html>
            <body>
                <h1>Products</h1>
                <p>Product list.</p>

                <a href="/about">About</a>
                <a href="./details">Details</a>
                <a href="https://example.com">External</a>
                <a>Missing href</a>

                <img src="/logo.png">
                <img src="./photo.jpg">
                <img src="https://cdn.example.com/banner.png">
                <img alt="Missing src">
            </body>
        </html>
        """

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": input_url,
            "heading": "Products",
            "first_paragraph": "Product list.",
            "outgoing_links": [
                "https://crawler-test.com/about",
                "https://crawler-test.com/products/details",
                "https://example.com",
            ],
            "image_urls": [
                "https://crawler-test.com/logo.png",
                "https://crawler-test.com/products/photo.jpg",
                "https://cdn.example.com/banner.png",
            ],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_falls_back_to_h2(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html>
            <body>
                <h2>Fallback Heading</h2>
            </body>
        </html>
        """

        actual = extract_page_data(input_body, input_url)

        self.assertEqual(actual["heading"], "Fallback Heading")

    def test_extract_page_data_prioritizes_h1_over_h2(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html>
            <body>
                <h2>Secondary Heading</h2>
                <h1>Primary Heading</h1>
            </body>
        </html>
        """

        actual = extract_page_data(input_body, input_url)

        self.assertEqual(actual["heading"], "Primary Heading")

    def test_extract_page_data_prioritizes_paragraph_inside_main(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html>
            <body>
                <p>Paragraph outside main.</p>
                <main>
                    <p>Paragraph inside main.</p>
                </main>
            </body>
        </html>
        """

        actual = extract_page_data(input_body, input_url)

        self.assertEqual(actual["first_paragraph"], "Paragraph inside main.")


if __name__ == "__main__":
    unittest.main()
