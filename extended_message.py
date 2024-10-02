import uuid

class ExtendedMessage:
    def __init__(self, role, content, sender, recipient, run_id=None):
        self.role = role
        self.content = content
        self.sender = sender
        self.recipient = recipient
        self.run_id = run_id or str(uuid.uuid4())

    def to_api_format(self):
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_api_format(cls, api_message, sender, recipient, run_id=None):
        return cls(api_message["role"], api_message["content"], sender, recipient, run_id)

    def get_run_id(self):
        return self.run_id
