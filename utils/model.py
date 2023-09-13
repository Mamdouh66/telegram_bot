import openai
import os
import urllib.request
import json

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
DATA_DIR = Path.cwd() / "responses"
DATA_DIR.mkdir(exist_ok=True)

def calling_dalle(prompt):
    response = openai.Image.create(
        prompt = prompt,
        n = 1,
        size = '512x512',
        response_format = 'b64_json'
    )
    return response

def creating_json_file(response, prompt):
    file_name = DATA_DIR / f"{prompt[:5]}-{response['created']}.json"
    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)
    return file_name

def get_image(prompt):
    response = calling_dalle(prompt)
    file_name = creating_json_file(response, prompt)
    return file_name