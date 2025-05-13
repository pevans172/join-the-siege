from werkzeug.datastructures import FileStorage
import openai

from src import ENV_VARIABLES


openai.api_key = ENV_VARIABLES["OPENAI_API_KEY"]


def classify_file(file: FileStorage) -> dict:
    filename = file.filename.lower()

    if filename == "":
        return {"msg": {"error": "No selected file"}, "code": 400}

    file_type = filename.rsplit(".", 1)[1].lower()

    if file_type not in ENV_VARIABLES["ALLOWED_EXTENSIONS"]:
        return {
            "msg": {
                "error": f"{file_type} is not allowed. Must be one of: {ENV_VARIABLES['ALLOWED_EXTENSIONS']}"
            },
            "code": 400,
        }

    file_class = "unknown_file"
    if "drivers_license" in filename:
        file_class = "drivers_licence"
    if "bank_statement" in filename:
        file_class = "bank_statement"
    if "invoice" in filename:
        file_class = "invoice"

    return {
        "msg": {"file_class": file_class},
        "code": 400,
    }
