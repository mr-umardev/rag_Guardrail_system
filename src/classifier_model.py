import joblib
import os

from sklearn.ensemble import RandomForestClassifier


class GuardrailClassifier:

    def __init__(self):

        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )


    def train(self, X, y):

        print("Training guardrail classifier...")

        print("Training samples:", len(X))

        self.model.fit(X, y)

        print("Training complete.")


    def predict(self, features):

        prediction = self.model.predict([features])[0]

        return prediction


    def predict_proba(self, features):

        prob = self.model.predict_proba([features])[0]

        return prob


    def save(self, path):

        joblib.dump(self.model, path)

        print("Guardrail model saved:", path)


    def load(self, path):

        if not os.path.exists(path):

            raise Exception(f"Guardrail model not found: {path}")

        self.model = joblib.load(path)

        print("Guardrail model loaded:", path)