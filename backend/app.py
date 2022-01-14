import os
from flask import Flask
# import os
# import json

from dotenv import load_dotenv

import pymongo

# import spacy
# from spacy.language import Language
# from spacy_langdetect import LanguageDetector


load_dotenv()




app = Flask(__name__)

mongo_uri = os.environ['MONGO_URI']

client = pymongo.MongoClient(mongo_uri)

tweets_db = client.tweets

# tweets_list2 = []


# def get_lang_detector(nlp, name):
#     return LanguageDetector()


# nlp = spacy.load("en_core_web_sm")
# Language.factory("language_detector", func=get_lang_detector)
# nlp.add_pipe('language_detector', last=True)




@app.route('/test', methods = ["GET"]) 
def test():

    return { "result" : "testing OK" }





@app.route('/get-locations', methods = ["GET"]) 
def get_locations():

    collection = tweets_db["location_hits"]

    location_data = list(collection.find())

    for location in location_data:
        del location["_id"]

    return { "result" : location_data }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5555)