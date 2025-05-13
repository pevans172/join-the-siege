from flask import Flask, request, jsonify
from src.classifier import classify_file

app = Flask(__name__)


@app.route("/classify_file", methods=["POST"])
def classify_file_route():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    resp = classify_file(file=request.files["file"])

    return jsonify(resp["msg"]), resp["code"]


if __name__ == "__main__":
    app.run(debug=True)
