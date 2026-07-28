import argparse
import json
import string
import pickle
import os
from nltk.stem import PorterStemmer


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


MOVIES_DATA = load_movies()
STOP_WORDS_DATA = load_stop_words()
TABLE_PUNCTUATION = str.maketrans("", "", string.punctuation)
STEMMER = PorterStemmer()


def preprocess(input: str):
    input = input.lower()
    input = input.translate(TABLE_PUNCTUATION)
    arr = input.split()
    arr = filter(lambda x: x not in STOP_WORDS_DATA, arr)
    arr = map(lambda x: STEMMER.stem(x), arr)

    return list(arr)


class InvertedIndex:
    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict = {}

    def __add_document(self, doc_id, text):
        text_arr = preprocess(text)

        for text in text_arr:
            if text in self.index:
                self.index[text].add(doc_id)
            else:
                self.index[text] = {doc_id}

    def get_documents(self, term):
        return self.index.get(term)

    def build(self):
        for movie in MOVIES_DATA:
            id = movie.get("id")
            self.docmap[id] = movie
            self.__add_document(id, f"{movie['title']} {movie['description']}")

    def save(self):
        os.makedirs("cache", exist_ok=True)

        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index, f)

        with open("cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)


def build_command():
    inverted_index = InvertedIndex()

    inverted_index.build()
    inverted_index.save()
    docs = inverted_index.get_documents("merida")
    print(f"First document for token 'merida' = {docs[0]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")
    subparsers.add_parser("build", help="Build inverted index")

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")

            found = []

            if not STOP_WORDS_DATA:
                return

            if not MOVIES_DATA:
                return

            query_arr = preprocess(args.query)

            for movie in MOVIES_DATA:
                title_movie = movie["title"]
                title_arr = preprocess(title_movie)

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

        case "build":
            build_command()

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
