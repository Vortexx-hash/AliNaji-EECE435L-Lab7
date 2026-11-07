"""The standalone Flask POST example from Lab 7."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    return jsonify({"sum": data["a"] + data["b"]})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
