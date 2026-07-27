import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")
            file_path = "data/movies.json"

            with open(file_path) as f:
                data: dict = json.load(f)

                movies = data.get("movies")

                found = []

                if not movies:
                    return

                for movie in movies:
                    title = movie["title"]
                    if args.query in title:
                        found.append(title)

                count = 0
                for title in found:
                    count += 1

                    if count > 5:
                        return

                    print(f"{count}: {title}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
