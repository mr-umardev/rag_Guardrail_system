class ConversationManager:

    def __init__(self):

        self.questions = []

    def add_user_input(self, text):

        self.questions.append(text)

    def is_ready(self):

        return len(self.questions) >= 3

    def get_topic(self):

        return " ".join(self.questions)

    def reset(self):

        self.questions = []