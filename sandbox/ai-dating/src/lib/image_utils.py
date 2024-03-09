import base64
import os

from langchain.schema import HumanMessage
from src.lib.message_utils import create_human_message

IMAGE_DIR = "/app/images/"

def get_images() -> list[str]:
    for _, _, filenames in os.walk(IMAGE_DIR):
        return filenames

def encode_image(name: str) -> bytes:
    image_path = f"{IMAGE_DIR}{name}"
    with open(image_path, mode="rb") as image_file:
        return base64.b64encode(image_file.read()).decode(encoding="utf-8")


def create_url_dict(name: str):
    base64_image = encode_image(name)
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}",
        },
    }

def create_image_message() -> HumanMessage:
    inputs = get_images()
    content = [ {"type": "text", "text": "Here are the images"}]
    for input_ in inputs:
        content.append(create_url_dict(input_))
    return create_human_message(content)
