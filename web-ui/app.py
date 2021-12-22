from itertools import count
from flask import Flask, render_template
import requests



app = Flask(__name__)





@app.route('/', methods = ["GET"]) 
def index():

    URL = "http://172.20.0.2:5555/latest-tweets"
    PARAMS = {'address':'hey'}
    r = requests.get(url = URL)
    data = r.json()
    return str(data)
    print(r.data)



    

    # return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=8080)