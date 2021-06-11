# Troll Classification API service


# API endpoints


There is a single POST endpoint that with provided tweet text, will return binary prediction and float probability of tweet being authored by russian troll.

Code is prepared for the authorisation via Authorisation Bearer, but this needs to be further developed.

Local deployment request:
```bash
curl --location --request POST 'http://127.0.0.1:8090/api/v1.0/troll_classifier' \
--header 'Authorization: Bearer TOP_SECRET' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tweet_text": "hello hello Trump and melon"
}'
```

Responce:
```JSON
{
    "is_troll": false,
    "is_troll_probability": 0.5426
}
```

# running & deployment


## runnig locally (for developement purposes)

This service assumes to be run in linux based OS.
It requires [`python3.8`](https://www.python.org/downloads/release/python-387/) and related `pip` to be installed, for example by running:
```bash
sudo apt-get install python3.8 python3-pip
```

To easily control the dependencies, a python virtual environemnt is used.
Creating one and installing dependencies inside, works as follows:
```bash
cd app_api
python3.8 -m venv venv # creating venv 
source venv/bin/activate # activating venv for current shell session
pip install -r requirements.txt #installing dependencies
```

```bash
python3.8 main.py #running locally, API is available on localhost
```


### To add/change python requirenments
```bash
#change reqirements.in with text editor, then:
pip-compile #will compile reqirements.in to reqirements.txt
pip-install -r requirements.txt
```
## runing in Docker

```bash
#building image:
docker build . -t troll-classification

#running locally:
docker run -p 8090:8090 troll-classification

```
