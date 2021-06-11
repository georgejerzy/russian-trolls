FROM python:3.8-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY app_api/main.py ./main.py
COPY app_api/requirements.txt ./requirements.txt
COPY artifacts ./artifacts
COPY russian_trolls ./russian_trolls
ENV ARTIFACTS_DIR ./artifacts/trolls_classifier_20210611T220639
ENV PORT 8090

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app