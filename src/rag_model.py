class RagModel:

    def generate(self, query, context, external_answer=None):

        if external_answer is not None:
            return external_answer

        return ""