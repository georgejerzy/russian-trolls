# russian-trolls-classifier
This is my attempt to build a classification model for the problem stated here:
https://www.kaggle.com/vikasg/russian-troll-tweets


## Project description

1. Interesting papers

https://paperswithcode.com/search?q_meta=&q_type=&q=russian+trolls
https://github.com/parkervg/troll-tweet-detector/blob/master/Trolliness.ipynb

2. Loading data & initial data exploration

- It seems that most of the numerical features are not very interesting - would be hard for those to be usefull in real world scenatio
in browsing millions of Twitter users.
- rest of the project will be focused on NLP based solution that should 
  be able to distinguish troll tweets vs. normal ones only based on text
- Please check notebooks for more notes:
  - 1_users_initial_eda.ipynb  
  - 2_tweets_initial_eda.ipynb 
  
- topic modelling would be valuable at this stage to answer the question of what
is specyfic for those tweets - that was unfrotunately skipped due to time limitation.

3. External dataset
- It would be quite time consuming to extract proper data over Twitter API,
thus I've decided to use already extracted blob of tweets as samples:
  https://archive.org/download/archiveteam-twitter-stream-2017-09
-   one can use `download_data.sh` script to download the extenal blob

4. Preprocessing
- to make training easier, a ready-to-use dataset csv file with both classes 
  was prepared,
- **it consist only english Tweets - that is a simplification,**
- one can use `create_datatet.sh` script to prepare such a training set.
- `russian_trolls` python contains common classes, the code is being formatted with
`black` python formatter, with google docstring. 

5. Training 
- off-the shelf model was used in order to quicly reach the results, one can find 
  more details in `5_model_training_tensorflow` notebook.
- in practice, pre-trained DistilBERT model with it's tokeniser was used: https://huggingface.co/transformers/model_doc/distilbert.html
- **model was fine-tuned only on 20000 samples - that is another simplification
just to reach the results faster**
- the interpretation was practiced using shap library

Results of training 
- It seems that the prepared model right is trained to recognise a tweets related 
  to politics, not necessary the russian trolls tweets.
- Considering above, it still showes quite entertaining results and gives hope for 
  more precise results on bigger dataset and eventually more sophiscicated model.

6. API app

Please see `app_api/README.md` for more details.
![alt text](data/img_1.png "demo")

7. Demo app

Please see `app_demo/README.md` for more details.
![alt text](data/img.png "demo")


# Research environment setup

```bash
python3.8 -m venv venv
source venv/bin/activate

pip install pip-tools
pip-compile #if there were chages in reqirements.in
pip intsall -r reqirements.txt

python3.8  -m ipykernel install --user --name=russian-trolls

```



