import os
import pickle
import math
from typing import Any, Counter
from lib.data_loader import load_movies
from lib.preprocessing import preprocess


class InvertedIndex:
    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, Any] = {}
        self.term_frequencies: dict[int, Counter] = {}

    def __add_document(self, doc_id, text):
        text_arr = preprocess(text)

        for text in text_arr:
            if text in self.index:
                self.index[text].add(doc_id)
            else:
                self.index[text] = {doc_id}

            if doc_id in self.term_frequencies:
                self.term_frequencies[doc_id][text] += 1
            else:
                self.term_frequencies[doc_id] = Counter([text])

    def get_tf(self, doc_id, term):
        if doc_id in self.term_frequencies:
            return self.term_frequencies[doc_id][term]
        else:
            return 0

    def get_documents(self, term):
        arr = self.index.get(term)

        if not arr:
            return

        sorted_arr = sorted(arr)

        return list(sorted_arr)

    def build(self):
        movies_data = load_movies()
        for movie in movies_data:
            id = movie.get("id")
            self.docmap[id] = movie
            self.__add_document(id, f"{movie['title']} {movie['description']}")

    def get_bm25_idf(self, term: str) -> float:
        # term must be single token

        total_doc = len(self.docmap)
        document_frequency = len(self.get_documents(term) or [])

        bm25_idf = math.log(
            (total_doc - document_frequency + 0.5) / (document_frequency + 0.5) + 1
        )

        return bm25_idf

    def save(self):
        os.makedirs("cache", exist_ok=True)

        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index, f)

        with open("cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)

        with open("cache/term_frequencies.pkl", "wb") as f:
            pickle.dump(self.term_frequencies, f)

    def load(self):
        try:
            with open("cache/index.pkl", "rb") as f:
                self.index = pickle.load(f)

            with open("cache/docmap.pkl", "rb") as f:
                self.docmap = pickle.load(f)

            with open("cache/term_frequencies.pkl", "rb") as f:
                self.term_frequencies = pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError()
