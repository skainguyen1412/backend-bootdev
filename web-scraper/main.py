import sys


def main():
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


if __name__ == "__main__":
    main()
