from typing import List
from image_data import ImageData
from content_constructor import *
class Thread:
    def __init__(self, id):
        self.id = id
        self.conversation = []

    def add_user_message(self, text: str, images: List[ImageData] = []):
     
        content = [text_content(text)]
        for image in images:
            content.append(image_content(image.media_type,image.base64_data))
        
        self.conversation.append({"role": "user", "content": content})
        return {"role": "user", "content": content}

    def add_assistant_message(self, content):
        self.conversation.append({"role": "assistant", "content": content})

    def get_conversation(self):
        return self.conversation

    def get_id(self):
        return self.id
