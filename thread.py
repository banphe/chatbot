import base64
import os

class Thread:
    def __init__(self, id):
        self.id = id
        self.conversation = []

    def add_user_message(self, text, image_paths=[]):
        content = [{'type': "text", "text": text}]
        
        for image_path in image_paths:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode("utf-8")
                file_extension = os.path.splitext(image_path)[1]
                image_media_type = self.get_media_type(file_extension)
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_base64
                    }
                })
        
        self.conversation.append({"role": "user", "content": content})
        return {"role": "user", "content": content}

    def add_assistant_message(self, content):
        self.conversation.append({"role": "assistant", "content": content})

    def get_conversation(self):
        return self.conversation

    def get_id(self):
        return self.id

    @staticmethod
    def get_media_type(file_extension):
        media_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return media_types.get(file_extension.lower(), 'image/jpeg')