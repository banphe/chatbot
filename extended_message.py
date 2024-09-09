class ExtendedMessage:
    def __init__(self, role, content, sender, recipient):
        self.role = role
        self.content = content
        self.sender = sender
        self.recipient = recipient

    def to_api_format(self):
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_api_format(cls, api_message, sender, recipient):
        return cls(api_message["role"], api_message["content"], sender, recipient)
