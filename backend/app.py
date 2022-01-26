import os
from flask import Flask, request
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





@app.route('/get_locations', methods = ["GET"]) 
def get_locations():

    collection = tweets_db["location_hits"]

    location_data = list(collection.find())

    # to add new cols in db

    # for location in location_data:
    #     collection.update_one({"location" : location["location"]}, 
    #                                 {"$set": {
    #                                     "disaster_type"   : None ,
    #                                     "additional-info" : None
    #                                 }})

    for location in location_data:
        del location["_id"]

    return { "result" : location_data }


@app.route('/new_location', methods = ["POST"]) 
def new_location():

    collection = tweets_db["location_hits"]

    coord_string = request.form['coordinates']

    coords = [float(x) for x in coord_string[slice(7, -2, 1)].split(",")]
    data = {
        "coords"     : coords,
        "location"   : request.form['location_name'], 
        "disaster_type"   : request.form['disaster_type'],
        "additional-info" : request.form['additional-info'],
    }
    print(data["coords"])

    check = collection.find_one({"location" : str(data["location"])})

    if check:
        if collection.find_one({"location" : str(data["location"]), "disaster_type" : str(data["disaster_type"])}):
            collection.update_one({"location" : str(data["location"]), "disaster_type" : str(data["disaster_type"])}, 
                                    {"$set": {"coords": data["coords"], "additional-info" : data["additional-info"]}})
        else:
            collection.insert_one(data)
    else:
        collection.insert_one(data)

    

    return "New disaster entry added!"

    # return { "result" : location_data }


if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0",port=5555)
    app.run(host='0.0.0.0',port=5555, debug=True)