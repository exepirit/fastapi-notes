FROM python:3.8

WORKDIR /root/
COPY ./app app
COPY ./database database
COPY config config
COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

