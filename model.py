import openai
import os
import urllib.request
import json

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
PROMPT = 'a potato with a face'
DATA_DIR = Path.cwd() / "responses"
DATA_DIR.mkdir(exist_ok=True)

response = openai.Image.create(
    prompt = PROMPT,
    n = 1,
    size = '1024x1024',
    response_format = 'b64_json'
)

file_name = DATA_DIR / f"{PROMPT[:5]}-{response['created']}.json"

with open(file_name, mode="w", encoding="utf-8") as file:
    json.dump(response, file)
file_name = DATA_DIR / f"{PROMPT[:5]}-{response['created']}.json"
