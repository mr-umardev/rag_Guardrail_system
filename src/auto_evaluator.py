import json

from main import initialize, run


def evaluate():

    retriever, guardrail = initialize()

    with open("tests/test_queries.json", "r") as f:
        test_data = json.load(f)

    total = 0
    correct = 0

    for item in test_data:

        query = item["query"]
        answer = item.get("answer", "")
        expected = item["expected"]

        print("\nQuery:", query)

        result = run(query, answer, retriever, guardrail)

        predicted = result["decision"]

        print("Expected:", expected)
        print("Predicted:", predicted)

        total += 1

        if predicted == expected:
            correct += 1

    accuracy = correct / total if total > 0 else 0

    print("\nEvaluation Results")
    print("------------------")
    print("Total tests:", total)
    print("Correct:", correct)
    print("Accuracy:", accuracy)


if __name__ == "__main__":
    evaluate()