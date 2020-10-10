FROM python:3.8
WORKDIR /biomarker-annotation-webtool/api

EXPOSE 5000

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "api.py", "--host=0.0.0.0"]

