import io
import json
import os
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from loguru import logger
from PIL import Image

load_dotenv()

# setup logfile sink in loguru
logger.add("app.log")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "models/gemini-2.0-flash"
PROMPT = """
Read the following image and extract some structured data from it.
Return in a format of JSON only. Do not add any other text or explanation.

Extract the following fields:
- Name
- Address
- NIK Number
- Date of Birth
"""
IMAGE_FOLDER = "images"

app = Flask(__name__)


class FailedFormRead(Exception):
    pass


def read_form(image: Image.Image) -> dict:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(
        [PROMPT, image],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
    answer = response.text
    logger.info(f"LLM response: {answer}")
    answer = answer.replace("```json", "").replace("```", "")
    try:
        data_parsed = json.loads(answer)
    except json.JSONDecodeError as e:
        raise FailedFormRead("Failed to parse JSON response from LLM") from e
    logger.info(f"Parsed data: {data_parsed}")
    return data_parsed


def save_image(image: Image.Image) -> None:
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".png"
    image.save(os.path.join(IMAGE_FOLDER, filename))


@app.route("/read-image", methods=["POST"])
def read_image_form():
    try:
        image = Image.open(io.BytesIO(request.data))
    except Exception as e:
        logger.exception(f"Failed to open image: {e}")
        return jsonify({"error": "Failed to open image"}), 400

    save_image(image)

    try:
        data = read_form(image)
    except FailedFormRead as e:
        logger.exception(f"Failed to parse JSON: {e}")
        return jsonify({"error": str(e)}), 400

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)
