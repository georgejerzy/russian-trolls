FROM python:3.8
EXPOSE 8501
WORKDIR /app
COPY app_demo/requirements.txt ./requirements.txt
COPY app_demo/main.py ./main.py
COPY artifacts ./artifacts
COPY russian_trolls ./russian_trolls
ENV ARTIFACTS_DIR ./artifacts/trolls_classifier_20210611T220639

RUN pip3 install -r requirements.txt
CMD streamlit run app.py

