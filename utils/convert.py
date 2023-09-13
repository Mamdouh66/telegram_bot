import json
from base64 import b64decode
from pathlib import Path

def convert_to_image(filename):
    DATA_DIR = Path.cwd() / "responses"
    JSON_FILE = DATA_DIR / f"{filename}"
    IMAGE_DIR = Path.cwd() / "images" / JSON_FILE.stem
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    with open(filename, mode="r", encoding="utf-8") as file:
        response = json.load(file)

    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{filename.stem}-{index}.png"
        with open(image_file, mode="wb") as png:
            png.write(image_data)
    
    return image_file
