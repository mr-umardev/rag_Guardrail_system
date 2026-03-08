from document_loader import load_documents, chunk_documents
from vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.store = VectorStore()

        index_loaded = self.store.load_index()

        if not index_loaded:

            docs = load_documents()

            chunks = chunk_documents(docs)

            self.store.build_index(chunks)


    def retrieve(self, query):

        results = self.store.search(query)

        return results