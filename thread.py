from typing import List
from image_data import ImageData
from content_constructor import *
from extended_message import ExtendedMessage
class Thread:
    def __init__(self, id):
        self.id = id
        self.conversation = []
    def add_user_message(self, text: str, images: List[ImageData] = [], sender="user", recipient="assistant", run_id=None):
     
        content = [text_content(text)]
        for image in images:
            content.append(image_content(image.media_type,image.base64_data))
        
        message = ExtendedMessage("user", content, sender, recipient, run_id)
        self.conversation.append(message)
        return message.to_api_format()

    def add_assistant_message(self, content, sender="assistant", recipient="user", run_id=None):
        message = ExtendedMessage("assistant", content, sender, recipient, run_id)
        self.conversation.append(message)

    def add_tool_request_message(self, content, sender="system", recipient="assistant", run_id=None):
        message = ExtendedMessage("user", content, sender, recipient, run_id)
        self.conversation.append(message)

    def get_conversation(self):
        return [msg.to_api_format() for msg in self.conversation]
        #return self.conversation

    def get_full_conversation(self):
        return self.conversation
    
    def get_id(self):
        return self.id
