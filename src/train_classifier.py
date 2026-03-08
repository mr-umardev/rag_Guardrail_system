import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

from document_loader import load_documents, chunk_documents
from auto_data_generator import generate_training_data
from feature_extractor import FeatureExtractor
from classifier_model import GuardrailClassifier
from config import MODEL_PATH


def train():

    print("Loading documents...")

    docs = load_documents()

    chunks = chunk_documents(docs)

    print("Total chunks:", len(chunks))

    print("Generating training dataset...")

    dataset = generate_training_data(chunks)

    extractor = FeatureExtractor()

    clf = GuardrailClassifier()

    X = []
    y = []

    for q, c, a, label in dataset:

        features = extractor.extract(q, c, a)

        X.append(features)
        y.append(label)

    print("Total training samples:", len(X))

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42
    )

    print("Training guardrail classifier...")

    clf.train(X_train, y_train)

    print("Evaluating model...")

    preds = []

    for features in X_test:

        pred = clf.predict(features)

        preds.append(pred)

    f1 = f1_score(y_test, preds)

    print("Validation F1 Score:", f1)

    if f1 < 0.6:

        print("Warning: F1 score below required threshold (0.6)")
        print("Consider adding more training data.")

    else:

        print("F1 score meets required threshold.")

    clf.save(MODEL_PATH)

    print("Guardrail model saved to:", MODEL_PATH)

    print("Training complete.")


if __name__ == "__main__":

    train()