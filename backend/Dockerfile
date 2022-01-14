# FROM ubuntu 

# RUN apt-get update 
# RUN apt-get install -y python3-pip

# ADD . /code
# WORKDIR /code
# ARG CRYPTOGRAPHY_DONT_BUILD_RUST=1
# EXPOSE 8080

# RUN pip install -r requirements.txt

# RUN python3 -m spacy download en_core_web_sm


# CMD ["python3", "app.py"]


FROM python:3-alpine3.13

RUN apk update

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt

EXPOSE 5555

CMD ["python", "app.py"]
