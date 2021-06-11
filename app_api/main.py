import os
from flask import Flask, jsonify
from flask import request, abort, Response
from flask_httpauth import HTTPTokenAuth


app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

tokens = {
    "TOP_SECRET": "troll_classifier_token",
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.route("/api/v1.0/troll_classifier", methods=["POST"])
@auth.login_required
def get_cart():
    if not request.json:
        return Response(
            "JSON request body missing", status=400, mimetype="application/json"
        )
    if not request.json.get("tweet_text"):
        return Response(
            "tweet_text field missing.",
            status=400,
            mimetype="application/json",
        )

    tweet_text = request.json.get("tweet_text")
    # c = CartCreator(questionaire_answers)

    return jsonify({"is_troll": False, "is_troll_probability": 0.5})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8090)))
