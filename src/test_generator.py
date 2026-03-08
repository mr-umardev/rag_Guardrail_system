def generate_queries(docs):

    queries = []

    for doc in docs:

        sentences = doc.split(".")[:5]

        for s in sentences:

            if len(s) > 20:

                q = "How to fix " + s[:40]

                queries.append(q)

    return queries