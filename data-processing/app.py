from datetime import datetime
from tabnanny import check
from flask import Flask
import os
import json

from dotenv import load_dotenv


import spacy
# from spacy import displacy
from spacy.language import Language
from spacy.util import get_model_lower_version
from spacy_langdetect import LanguageDetector

import pymongo
import en_textcat_demo

from pathlib import Path

import requests

from flask_apscheduler import APScheduler


load_dotenv()

output_dir=Path('./location_model')

app = Flask(__name__)

mongo_uri = os.environ['MONGO_URI']

client = pymongo.MongoClient(mongo_uri)

tweets_db = client.tweets

scheduler = APScheduler()
scheduler.init_app(app)

app.config['SECRET_KEY'] = 'thisismysp'

tweets_list2 = []


def get_lang_detector(nlp, name):
    return LanguageDetector()


global nlp 
nlp  = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)


def write_locations_db(locations_list):

    collection = tweets_db["location_hits"]

    current_datetime = datetime.now()
    
    for location in locations_list:
        URL = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token=pk.eyJ1IjoiYWplc2htYXJ0aW4wMSIsImEiOiJja3lnNHplN28wdnNlMndtbHdmMDM1OHF0In0.qFZ4GUd-Aczp_qwJXUweIQ"
        # PARAMS = {'address':'hey'}
        r = requests.get(url = URL)
        data = r.json()
        try:
            coords = data["features"][0]['center']
        except:
            coords = []
        check_location = collection.find_one({"location": location})

        if check_location :
            hits = check_location["count"]
            collection.update_one({"location": location},{"$set": {"count": hits + 1, "last_hit" : current_datetime}}) # need to change current datetime to latest tweet
        else :

            location_hit_entry = {
                "location" : location,
                "count" : 1,
                "coords" : coords,
                "last_hit" : current_datetime # need to change current datetime to latest tweet
            }
            collection.insert_one(location_hit_entry)
    return locations_list

        
        






@app.route('/test', methods = ["GET"]) 
def test():

    return { "result" : "testing OK" }






# @app.route('/latest-tweets', methods = ["GET"]) 
def get_latest_tweets():
    global nlp
    date = datetime.now()
    
    date = date.strftime("%Y-%m-%d")
    # gets tweets and saves it in a jsonl format
    # os.system("snscrape --jsonl --max-results 1000 --since 2020-06-01 twitter-search 'killed OR dead OR disaster OR tragedy OR incident AND india' > text-query-tweets.json")
    os.system(f"snscrape --jsonl --max-results 1000 --since {date} twitter-search 'killed OR dead OR disaster OR tragedy OR incident AND india' > text-query-tweets.json")
    # print(count(tweets_list2)) 
 
    tweets = []
    for line in open('text-query-tweets.json', 'r'):
        tweet = json.loads(line)
        # isReliable, textBytesFound, details = cld2.detect("а неправильный формат идентификатора дн назад")
        # print(details)
        text_content = tweet["content"]
        doc = nlp(text_content) 
        detect_language = doc._.language
        english_flag = False

        #  filters tweets in english
        if detect_language["language"] == 'en' and detect_language['score'] >= 0.85:
            # english_flag = True
            # tweet["is_english"] = english_flag
            # print(tweet)

            
            tweets.append(tweet["content"])

    
    nlp2 = en_textcat_demo.load()

    docs = list(nlp2.pipe(tweets))

    nlp_updated = spacy.load(output_dir)

    result = []
    locations_list = []

    for doc in docs:
        # print(doc.text)
        # print()
        # print(ty)
        if doc.cats["DISASTER"] > 0.75:

            print(doc.text)
            loc_doc = nlp_updated(doc.text)
            for ent in loc_doc.ents:
                if ent.label_ == "LOC":
                    print(ent.label)
                    locations_list.append(str(ent))
            # result.append(doc.text)
            # text2= nlp(doc.text)
            # for word in text2.ents:
            #     # print(word.text,word.label_)
            #     # print(word.label_)

            #     if word.label_ == "GPE" and word.text not in locations_list:
            #         locations_list.append(word.text)
            #         print(doc.text)
    # displacy.render(doc, style="ent")
            # print(f"{doc.text}\n")
    # print(detect_language)
    # print({ "result" : result })
    
    # print("locations_list: ",locations_list)

    # for tweet_hit in locations_list:
    #     print("Loading from", output_dir)
    #     nlp_updated = spacy.load(output_dir)
    #     doc = nlp_updated(tweet_hit)
    #     for ent in doc.ents:
    #         if ent.label == "LOC":
    #             print(ent.label)
        # print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
    
   
    
    return { "result" : write_locations_db(locations_list) }







if __name__ == '__main__':

    # if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    scheduler.start()
    app.apscheduler.add_job(timezone="Asia/Calcutta", func=get_latest_tweets, trigger='cron', id="tweet_scraping",week='*',day_of_week='*', hour = '*', minute = '*' , second = 0)
    print(scheduler.get_job("tweet_scraping"))
    app.run(debug=True, host="0.0.0.0",port=6666)