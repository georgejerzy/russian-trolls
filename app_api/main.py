import os
from flask import Flask, jsonify
from flask import request, abort, Response
from flask_httpauth import HTTPTokenAuth
import sys

sys.path.insert(0, "..")
from russian_trolls import model_predict

classificator_pipeline = model_predict.load_pipeline(
    os.environ.get(
        "ARTIFACTS_DIR"
    )  # f.e. ../artifacts/trolls_classifier_20210611T220639
)


app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

tokens = {
    "TOP_SECRET": "troll_classifier_token",  # todo: here itegrate wiht some secret storage service
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
    prediction, probability = model_predict.predict_single_tweet(
        classificator_pipeline,
        tweet_text,
    )
    return jsonify({"is_troll": prediction, "is_troll_probability": probability})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8090)))
