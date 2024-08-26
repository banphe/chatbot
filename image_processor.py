import base64
import os
from typing import List
from streamlit.runtime.uploaded_file_manager import UploadedFile
from image_data import ImageData
from io import BytesIO
from PIL import Image

def get_media_type(file_extension: str) -> str:
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return media_types.get(file_extension.lower(), 'image/jpeg')

def process_image(file: UploadedFile) -> ImageData:
    image_data = file.read()
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    file_extension = os.path.splitext(file.name)[1]
    image_media_type = get_media_type(file_extension)
    return ImageData(image_base64, image_media_type)

def process_multiple_images(files: List[UploadedFile]) -> List[ImageData]:
    return [process_image(file) for file in files]

def base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_data))