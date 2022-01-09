import csv
import json


training_entry = {
                    "text" : None,
                     "cats" : { 
                                "DISASTER": None,
                                "OTHER": None
                              } 
                }


file = open('data-processing/assets/tweets.csv')
csvreader = csv.reader(file)

with open("data-processing/assets/disaster_tweets_training.jsonl", 'a') as outfile:

    for row in csvreader:
            # disaster_flag = None
            # other_flag = None

            print(row[-2],row[-1])

            training_entry["text"] = row[-2]

            if row[-1] == '1' :
                training_entry["cats"]["DISASTER"] = 1.0
                training_entry["cats"]["OTHER"] = 0.0
            else:
                training_entry["cats"]["DISASTER"] = 0.0
                training_entry["cats"]["OTHER"] = 1.0

            # {"text":"Node.js: Produce docs files","cats":{"DOCUMENTATION":0.0,"OTHER":1.0}}

            json.dump(training_entry, outfile)
            outfile.write('\n')
