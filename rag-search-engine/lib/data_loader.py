import json

BM25_K1 = 1.5


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
