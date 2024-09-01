def text_content(text: str):
    return {'type': 'text', 'text': text}

def image_content(media_type: str, data: str):
    return {'type': 'image', 'source': {'type': 'base64', 'media_type': media_type, 'data': data}}

def tool_use_content(id: str, name: str, input: str):
    return {'type': 'tool_use', 'id': id, 'name': name, 'input': input}

def tool_result_content(tool_use_id, content, is_error=False):
    return {'type': 'tool_result', 'tool_use_id': tool_use_id, 'is_error': is_error, 'content': content}

