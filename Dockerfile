FROM python:3.8
WORKDIR backend/

EXPOSE 5000

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "api.py"]

