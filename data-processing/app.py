from flask import Flask
import os
import json



import spacy
from spacy import displacy
from spacy.language import Language
from spacy.util import get_model_lower_version
from spacy_langdetect import LanguageDetector

import en_textcat_demo



app = Flask(__name__)


tweets_list2 = []


def get_lang_detector(nlp, name):
    return LanguageDetector()


global nlp 
nlp  = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)




@app.route('/test', methods = ["GET"]) 
def test():

    return { "result" : "testing OK" }






@app.route('/latest-tweets', methods = ["GET"]) 
def get_latest_tweets():
    global nlp
    # gets tweets and saves it in a jsonl format
    os.system("snscrape --jsonl --max-results 500 --since 2020-06-01 twitter-search 'killed OR dead OR disaster OR tragedy OR incident' > text-query-tweets.json")
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

    result = []
    locations_list = []

    for doc in docs:
        # print(doc.text)
        # print()
        # print(ty)
        if doc.cats["DISASTER"] > 0.75:
            # result.append(doc.text)
            text2= nlp(doc.text)
            for word in text2.ents:
                # print(word.text,word.label_)
                # print(word.label_)

                if word.label_ == "GPE" and word.text not in locations_list:
                    locations_list.append(word.text)
                    print(doc.text)
    # displacy.render(doc, style="ent")
            # print(f"{doc.text}\n")
    # print(detect_language)
    # print({ "result" : result })
    

    

    return { "result" : locations_list }






if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=6666)