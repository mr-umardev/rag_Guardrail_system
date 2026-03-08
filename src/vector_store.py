import faiss
import numpy as np
import os
import pickle

from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.index = None
        self.documents = []

        self.index_path = "models/vector_index.faiss"
        self.docs_path = "models/chunks.pkl"


    def build_index(self, documents):

        print("Building vector index...")

        embeddings = self.model.encode(documents)

        embeddings = np.array(embeddings).astype("float32")

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)

        self.index.add(embeddings)

        self.documents = documents

        self.save_index()


    def save_index(self):

        if self.index is not None:

            faiss.write_index(self.index, self.index_path)

            with open(self.docs_path, "wb") as f:
                pickle.dump(self.documents, f)

            print("Vector index saved:", self.index_path)


    def load_index(self):

        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):

            print("Loading existing vector index...")

            self.index = faiss.read_index(self.index_path)

            with open(self.docs_path, "rb") as f:
                self.documents = pickle.load(f)

            return True

        return False


    def search(self, query):

        if self.index is None:
            raise Exception("Vector index not initialized")

        q_emb = self.model.encode([query])

        q_emb = np.array(q_emb).astype("float32")

        distances, ids = self.index.search(q_emb, 5)

        best_chunk = None
        best_score = None

        for i, d in zip(ids[0], distances[0]):

            if i < 0 or i >= len(self.documents):
                continue

            chunk = self.documents[i]

            score = 1 / (1 + d)

            if best_score is None or score > best_score:

                best_score = score
                best_chunk = chunk

        if best_score is not None and best_score > 0.20:

            return [best_chunk]

        return []