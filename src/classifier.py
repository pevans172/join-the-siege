from werkzeug.datastructures import FileStorage
import base64
import openai

from src import ENV_VARIABLES


openai_client = openai.OpenAI(api_key=ENV_VARIABLES["OPENAI_API_KEY"])


def openai_classifier(file_bytes: bytes, file_type: str) -> str:
    if file_type in ENV_VARIABLES["ALLOWED_GENERAL_EXTENSIONS"]:
        prompt = (
            f"Given the following bytes from a file that has a file extension {file_type}, classify it into one of these categories: "
            f"{', '.join(ENV_VARIABLES['DOCUMENT_TYPES'])}.\n\n"
            f"Bytes:\n{file_bytes}\n\n"
            f"Category:"
        )

        response = openai_client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        return response.choices[0].message.content.strip()

    if file_type in ENV_VARIABLES["ALLOWED_IMAGE_EXTENSIONS"]:
        # Use GPT-4 with vision
        base64_image = base64.b64encode(file_bytes).decode("utf-8")

        prompt = (
            f"This is an image file. Based on its contents, classify it into one of these categories: "
            f"{', '.join(ENV_VARIABLES['DOCUMENT_TYPES'])}.\n\n"
            f"Category:"
        )

        response = openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{file_type};base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=50,
            temperature=0,
        )
        return response.choices[0].message.content.strip()

    return "unknown_file"


def classify_file(file: FileStorage) -> dict:
    filename = file.filename.lower()

    if filename == "":
        return {"msg": {"error": "No selected file"}, "code": 400}

    file_type = filename.rsplit(".")[-1].lower()

    allowed_extensions = (
        ENV_VARIABLES["ALLOWED_GENERAL_EXTENSIONS"]
        | ENV_VARIABLES["ALLOWED_IMAGE_EXTENSIONS"]
    )
    if file_type not in allowed_extensions:
        return {
            "msg": {
                "error": f"{file_type} is not allowed. Must be one of: {allowed_extensions}"
            },
            "code": 400,
        }

    file_class = openai_classifier(file_bytes=file.read(), file_type=file_type)

    return {
        "msg": {"file_class": file_class},
        "code": 200,
    }
