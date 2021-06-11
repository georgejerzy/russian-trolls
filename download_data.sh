#!/bin/bash

echo "This script will download and preprocess data needed for training the model."

mkdir data  || true

echo "Checking existence of off-line provided dataset."
for FILE in ./data/provided_offline/tweets.csv ./data/provided_offline/users.csv
do
  if [ -f "$FILE" ]; then
      echo "$FILE exists."
  else
      echo "$FILE does not exist. Please provide manually. Aborting." && exit
  fi
done

echo "Downloading additional tweeter dataset."

cd data || exit

FILE=./twitter-stream-2017-09-10.tar
if [ -f "$FILE" ]; then
    echo "$FILE exists. Proceeding"
else
    echo "$FILE does not exist. Will download ~500MB." && exit
    wget https://archive.org/download/archiveteam-twitter-stream-2017-09/twitter-stream-2017-09-10.tar
fi

mkdir twitter-stream   || true
tar -xvf twitter-stream-2017-09-10.tar  -C twitter-stream