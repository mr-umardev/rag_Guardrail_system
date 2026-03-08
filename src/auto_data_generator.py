import random


def generate_training_data(chunks):

    dataset = []

    query_templates = [
        "not working",
        "issue",
        "problem",
        "error",
        "not responding",
        "failure",
        "unable to use",
        "crashing",
        "broken"
    ]

    for chunk in chunks:

        words = chunk.split()

        if len(words) < 30:
            continue

        topic = words[0]

        # generate positive samples
        for _ in range(20):

            query = topic + " " + random.choice(query_templates)

            answer = chunk[:200]

            dataset.append((query, chunk, answer, 1))

        # generate negative samples
        for _ in range(20):

            wrong_chunk = random.choice(chunks)

            query = topic + " " + random.choice(query_templates)

            dataset.append((query, wrong_chunk, answer, 0))

    return dataset