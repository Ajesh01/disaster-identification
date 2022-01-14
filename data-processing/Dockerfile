FROM ubuntu 

RUN apt-get update 
RUN apt-get install -y python3-pip

ADD . /code
WORKDIR /code
ARG CRYPTOGRAPHY_DONT_BUILD_RUST=1
EXPOSE 6666

RUN pip install -r requirements.txt

# RUN python3 -m spacy download en_core_web_sm

RUN python3 -m spacy download en_core_web_sm

CMD ["python3", "app.py"]