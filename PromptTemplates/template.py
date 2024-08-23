import re

class Template:
    def __init__(self, name, description, start_tag, end_tag, pre_text, post_text):
        self.name = name
        self.description = description
        self.start_tag = start_tag
        self.end_tag = end_tag
        self.pre_text = pre_text
        self.post_text = post_text

    def apply(self, message):
        return f"{self.pre_text}\n{self.start_tag}\n{message}\n{self.end_tag}\n{self.post_text}".strip()

    def extract(self, message):
        pattern = f"{re.escape(self.start_tag)}(.*?){re.escape(self.end_tag)}"
        match = re.search(pattern, message, re.DOTALL)
        if match:
            return match.group(1).strip()
        return message  # Return original message if no tags found