import streamlit as st
import sys, os
import matplotlib.pyplot as pl
from streamlit import components

sys.path.insert(0, "..")
from russian_trolls import model_predict

import shap

classificator_pipeline = model_predict.load_pipeline(
    os.environ.get(
        "ARTIFACTS_DIR"
    )  # f.e. ../artifacts/trolls_classifier_20210611T220639
)
explainer = shap.Explainer(classificator_pipeline, classificator_pipeline.tokenizer)


# Add title on the page
st.title("Tweeter trolls classification")

# Ask user for input text
input_sent = st.text_input(
    "Input tweet", "WATCH🚨 Terrorist experts: Obama is the founder of ISIS"
)

st.write(model_predict.predict_single_tweet(classificator_pipeline, input_sent))


# todo: this is what I really wanted this app to show, unfortunately, this particular methid from shap library deesnt return plot object nor html
shap.plots.text(
    explainer([input_sent])[:, :, "LABEL_1"],
)
