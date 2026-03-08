from classifier_model import GuardrailClassifier
from feature_extractor import FeatureExtractor
from config import MODEL_PATH


class DecisionEngine:

    def __init__(self):

        self.clf = GuardrailClassifier()

        self.clf.load(MODEL_PATH)

        self.extractor = FeatureExtractor()


    def decide(self, query, context, answer):

        features = self.extractor.extract(query, context, answer)

        probs = self.clf.predict_proba(features)

        stop_prob = probs[0]
        accept_prob = probs[1]

        similarity = float(features[0])

        query_len = len(query.split())

        print("Guardrail Features:", features)
        print("Guardrail Confidence:", probs)

        # Strong semantic match
        if similarity > 0.30:

            decision = "ACCEPT"

        # Short queries allowed slightly weaker similarity
        elif query_len <= 2 and similarity > 0.15:

            decision = "ACCEPT"

        # Classifier confidence
        elif accept_prob > 0.55:

            decision = "ACCEPT"

        else:

            decision = "STOP_SESSION"

        return {
            "decision": decision,
            "features": features,
            "confidence": probs.tolist()
        }