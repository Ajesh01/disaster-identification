from itertools import count
from shutil import register_unpack_format
from flask import Flask, render_template
import requests



app = Flask(__name__)





@app.route('/', methods = ["GET"]) 
def index():

    URL = "http://172.20.0.3:5555/get_locations"
    # PARAMS = {'address':'hey'}
    r = requests.get(url = URL)
    data = r.json()
    # return str(data)
    # print(r.data)

    return render_template("index.html", result = data)



    

    # return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=8080)