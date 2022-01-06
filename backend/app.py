from flask import Flask
# import os
# import json



# import spacy
# from spacy.language import Language
# from spacy_langdetect import LanguageDetector





app = Flask(__name__)


# tweets_list2 = []


# def get_lang_detector(nlp, name):
#     return LanguageDetector()


# nlp = spacy.load("en_core_web_sm")
# Language.factory("language_detector", func=get_lang_detector)
# nlp.add_pipe('language_detector', last=True)




@app.route('/test', methods = ["GET"]) 
def test():

    return { "result" : "testing OK" }






# @app.route('/latest-tweets', methods = ["GET"]) 
# def get_latest_tweets():

#     # gets tweets and saves it in a jsonl format
#     os.system("snscrape --jsonl --max-results 50 --since 2020-06-01 twitter-search 'flood' > text-query-tweets.json")
#     # print(count(tweets_list2)) 
 
#     tweets = []
#     for line in open('text-query-tweets.json', 'r'):
#         tweet = json.loads(line)
#         # isReliable, textBytesFound, details = cld2.detect("а неправильный формат идентификатора дн назад")
#         # print(details)
#         text_content = tweet["content"]
#         doc = nlp(text_content) 
#         detect_language = doc._.language
#         english_flag = False

#         #  filters tweets in english
#         if detect_language["language"] == 'en' and detect_language['score'] >= 0.85:
#             english_flag = True
#             tweet["is_english"] = english_flag
#             tweets.append(tweet)


        
#     # pprint.pprint(tweets[0])




#     print(detect_language)

#     return { "result" : "success" }


# import en_textcat_demo

# nlp = en_textcat_demo.load()
# text = ['yea right, so funny', 'You forgot "Am I a joke to you" guy', "Pretty ballsey for Ted to mouth off to his bosses like that.", "I’m sure she is going to make an absolutely stellar cop, with no power trip agenda whatsoever", "Shut up, college boy!!"]

# docs = list(nlp.pipe(text))
# result = []
# for doc in docs:
#     print(doc.text)
#     print(f"{doc.cats}\n")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5555)