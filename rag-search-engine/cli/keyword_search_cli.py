import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.inverted_index import InvertedIndex
from lib.preprocessing import preprocess, single_token


def build_command():
    inverted_index = InvertedIndex()
    inverted_index.build()
    inverted_index.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")
    subparsers.add_parser("build", help="Build inverted index")

    tf_parser = subparsers.add_parser("tf", help="Get term frequencies")
    tf_parser.add_argument("doc_id", type=int, help="Document id")
    tf_parser.add_argument("term", type=str, help="Term")

    idf_parser = subparsers.add_parser("idf", help="Inverse Document Frequency")
    idf_parser.add_argument("term", type=str, help="Term")

    tfidf = subparsers.add_parser("tfidf", help="Search base on tf-idf")
    tfidf.add_argument("doc_id", type=int, help="Document id")
    tfidf.add_argument("term", type=str, help="Term")

    args = parser.parse_args()

    inverted_index = InvertedIndex()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")

            inverted_index.load()

            if not inverted_index.index:
                print("Index not exist")
                exit(1)

            queries = preprocess(args.query)
            count = 0

            for query in queries:
                ids = inverted_index.get_documents(query)

                if not ids:
                    continue

                for id in ids:
                    count += 1

                    if count > 5:
                        break

                    movie = inverted_index.docmap.get(id)

                    if movie:
                        print(movie["title"], id)

        case "build":
            build_command()

        case "tf":
            doc_id = args.doc_id
            term = args.term
            inverted_index.load()
            single_token_term = single_token(term)
            print(inverted_index.get_tf(doc_id, single_token_term))

        case "idf":
            inverted_index.load()
            single_term = single_token(args.term)
            total_doc_count = len(inverted_index.docmap)
            term_match_doc_count = len(inverted_index.get_documents(single_term) or [])

            idf = math.log((total_doc_count + 1) / (term_match_doc_count + 1))
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")

        case "tfidf":
            inverted_index.load()
            single_token_term = single_token(args.term)
            tf = inverted_index.get_tf(args.doc_id, single_token_term)
            single_term = single_token(args.term)
            total_doc_count = len(inverted_index.docmap)
            term_match_doc_count = len(inverted_index.get_documents(single_term) or [])
            idf = math.log((total_doc_count + 1) / (term_match_doc_count + 1))

            tf_idf = tf * idf

            print(
                f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf:.2f}"
            )

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
