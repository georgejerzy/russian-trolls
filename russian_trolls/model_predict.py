import transformers
from transformers import TFDistilBertForSequenceClassification, AutoTokenizer
from transformers import pipeline
from tweets_preprocessor import TweetsPreprocessor
import shap


def load_pipeline(artifact_dir: str) -> transformers.Pipeline:
    """
    Loads transformers pipeline from file.
    Args:
        artifact_dir: directory with tockeniser and model artifacts
    Returns:
        prediction pipeline
    """
    tokenizer_loaded = AutoTokenizer.from_pretrained(artifact_dir)
    model_loaded = TFDistilBertForSequenceClassification.from_pretrained(artifact_dir)
    return pipeline(
        "text-classification",
        model=model_loaded,
        tokenizer=tokenizer_loaded,
        return_all_scores=True,
    )


def predict_single_tweet(
    classificator_pipeline: pipeline, tweet_text: str, threshold: float = 0.5
) -> (bool, float):
    """
    Performes prediction of provided classificator_pipeline for a single tweet.
    #todo: refactor this function to handle list of inputs
    Args:
        classificator_pipeline: pipeline
        tweet_text: tweet text
        threshold: treshould applied on probability score

    Returns:
        (prediction, probability)
    """
    clean_text = TweetsPreprocessor.cleaner(tweet_text)
    output = classificator_pipeline(clean_text, truncation=True)
    for i in output[0]:
        if i["label"] == "LABEL_1":
            probability = i["score"]
            prediction = i["score"] > threshold
            return prediction, probability

    raise KeyError("Could not parse model output")


def get_shap_values(
    classificator_pipeline: pipeline, tweet_text: str
) -> shap._explanation.Explanation:
    """
    Calculates shapley values of provided tweet tweet_text.
    Args:
        classificator_pipeline: pipeline
        tweet_text: tweet text

    Returns:
        shapley values explanation object - to be used as shap.plots.text(shap_values[:,:,"LABEL_1"])
    """
    explainer = shap.Explainer(classificator_pipeline, classificator_pipeline.tokenizer)
    return explainer([tweet_text])


if __name__ == "__main__":

    classificator_pipeline = load_pipeline(
        "../artifacts/trolls_classifier_20210611T220639"
    )

    print(
        predict_single_tweet(
            classificator_pipeline,
            "WATCH🚨 Terrorist experts: Obama is the founder of ISIS",
        )
    )

    print(
        get_shap_values(
            classificator_pipeline,
            "WATCH🚨 Terrorist experts: Obama is the founder of ISIS",
        )
    )
