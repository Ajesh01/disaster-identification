import csv
import json
from os import lchflags
import random
import pandas as pd




file = open('../assets/worldcities.csv')
csvreader = csv.reader(file)
locations = []
with open("../assets/location_training.jsonl", 'a') as outfile:

        for row in csvreader:
                # disaster_flag = None
                # other_flag = None
                if row[4] == "India":
                        locations.append(row[0])
                # print(row[-2],row[-1])


# file2 = open('../assets/tweets.csv')
# csvreader2 = csv.reader(file2)
# print(locations)

modified_tweets = []

i = 0

df = pd.read_csv('../assets/tweets.csv')

# if df.iloc[5, 6]:
# {"text": "text", "cats": {"DISASTER": 0.0, "OTHER": 1.0}}
# ("Pizza is a common fast food.", {"entities": [(0, 5, "FOOD")]})


with open("../assets/location_training.jsonl", 'a') as outfile:

        for i2 in locations:
                training_template  =  [ None, {"entities": []}]

                tweet = df.iloc[i , -2]
                split_tweet = tweet.split()
                split_tweet.insert(random.randrange(0,len(split_tweet), 2), i2) 
                new_tweet = ""
                for word in split_tweet:
                        new_tweet = new_tweet+" "+word
                # print(split_tweet, i2)
                # print(new_tweet)
                modified_tweets.append(new_tweet)

                print(new_tweet.index(i2))
                print(new_tweet[new_tweet.index(i2):new_tweet.index(i2)+len(i2)])
                # print(df.iloc[i+1 , -2])
                # modified_tweets.append(df.iloc[i+1 , -2])
                training_template[0] = new_tweet
                training_template[1]["entities"].append([new_tweet.index(i2),new_tweet.index(i2)+len(i2),"LOCATION"])
                

                json.dump({"data" : training_template}, outfile)
                outfile.write('\n')
                
                i += 2



# for tweet in modified_tweets:



        
# print(len(modified_tweets), len(locations))
# for loc in locations:
#         # print(location)
#         for i, row  in enumerate(csvreader2):
#                 print(loc)
#                 if i == locations.index(loc):
#                         tweet = row[-2]
#                         split_tweet = tweet.split()
#                         split_tweet.insert(random.randrange(0,len(split_tweet), 2), loc) 
#                         new_tweet = ""
#                         for word in split_tweet:
#                                 new_tweet+=word
#                         print(split_tweet, loc)
#                         print(new_tweet)
                
# print(locations)
