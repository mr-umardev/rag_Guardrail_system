from retriever import Retriever
from decision_engine import DecisionEngine


def normalize_query(q):

    q = q.lower()

    replacements = {
        "amhaving": "having",
        "gut": "git",
        "not work": "not working",
        "issue with": "issue",
        "problem with": "issue"
    }

    for k, v in replacements.items():
        q = q.replace(k, v)

    return q


def initialize():

    print("Starting Guardrail Validation System...")

    retriever = Retriever()
    guardrail = DecisionEngine()

    print("System initialized successfully.")

    return retriever, guardrail


def run(query, answer, retriever, guardrail):

    query = normalize_query(query)

    docs = retriever.retrieve(query)

    print("Retrieved chunks:", len(docs))

    if not docs:

        return {"decision": "STOP_SESSION"}

    context = " ".join(docs)

    result = guardrail.decide(query, context, answer)

    return result


if __name__ == "__main__":

    retriever, guardrail = initialize()

    while True:

        query = input("User Query: ")

        if query.lower() in ["exit", "quit"]:

            print("Exiting system.")
            break

        answer = input("Model Generated Answer: ")

        result = run(query, answer, retriever, guardrail)

        print("Validation Decision:", result)