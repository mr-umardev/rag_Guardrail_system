import pickle
import os

FEEDBACK_PATH = "models/feedback_data.pkl"


def load_feedback():

    if os.path.exists(FEEDBACK_PATH):

        with open(FEEDBACK_PATH, "rb") as f:
            return pickle.load(f)

    return []


def save_feedback(data):

    with open(FEEDBACK_PATH, "wb") as f:
        pickle.dump(data, f)


def record_feedback(features, label):

    data = load_feedback()

    data.append((features, label))

    save_feedback(data)

    print("Feedback stored.")