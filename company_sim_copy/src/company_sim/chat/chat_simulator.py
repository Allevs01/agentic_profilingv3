class ChatSimulator:
    def __init__(self):
        self.messages = []

    def post(self, author, text):
        self.messages.append(f"{author}: {text}")

    def read(self):
        return "\n".join(self.messages)

    def seed(self, messages):
        for author, text in messages:
            self.post(author, text)
