import argparse
import json
import string


def load_movies():
    with open("data/movies.json") as f:
        try:
            return json.load(f).get("movies")
        except Exception as e:
            raise Exception(f"Lỗi nạp movies.json: {e}")


def load_stop_words():
    with open("data/stopwords.txt") as f:
        try:
            return f.read().splitlines()
        except Exception as e:
            raise Exception(f"Lỗi nạp stopwords.txt: {e}")


movies_data = load_movies()
stop_words_data = load_stop_words()
table_punctation = str.maketrans("", "", string.punctuation)


def preprocess(input: str):
    input = input.lower()
    input = input.translate(table_punctation)
    arr = input.split()
    arr = list(filter(lambda x: x not in stop_words_data, arr))

    return arr


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

            found = []

            if not stop_words_data:
                return

            if not movies_data:
                return

            for movie in movies_data:
                title_movie = movie["title"]
                title_arr = preprocess(title_movie)
                query_arr = preprocess(args.query)

                for query in query_arr:
                    found_match = False
                    for title in title_arr:
                        if query in title:
                            found.append(title_movie)
                            found_match = True
                            break
                    if found_match:
                        break

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
