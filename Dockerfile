FROM python:3.8
WORKDIR backend/

EXPOSE 5000

COPY requirements.txt .

RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y

RUN pip install -r requirements.txt

CMD ["python", "api.py"]

