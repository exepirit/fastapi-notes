FROM python:3.7

WORKDIR /root/
COPY ./app app
COPY ./database database
COPY config.py requirements.txt ./
RUN python3 -m pip install -r requirements.txt 

EXPOSE 80
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

