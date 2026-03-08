from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class FeatureExtractor:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")


    def similarity(self, emb1, emb2):

        score = cosine_similarity(emb1, emb2)[0][0]

        return score


    def extract(self, query, context, answer):

        if not context:

            return [0, 0, 0, len(query.split())]

        # Encode once
        query_emb = self.model.encode([query])
        context_emb = self.model.encode([context])

        qc = self.similarity(query_emb, context_emb)

        if answer:

            answer_emb = self.model.encode([answer])

            ac = self.similarity(answer_emb, context_emb)

            qa = self.similarity(query_emb, answer_emb)

        else:

            ac = 0
            qa = 0

        query_len = len(query.split())

        return [qc, ac, qa, query_len]