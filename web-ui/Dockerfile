FROM python:3-alpine3.13

RUN apk update

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt

CMD ["python", "app.py"]