from itertools import count
from shutil import register_unpack_format
from flask import Flask, redirect, render_template, request
import requests



app = Flask(__name__)





@app.route('/', methods = ["GET"]) 
def index():

    URL = "http://backend-service:5555/get_locations"
    # PARAMS = {'address':'hey'}
    r = requests.get(url = URL)
    data = r.json()
    # return str(data)
    # print(r.data)

    return render_template("index.html", result = data)



    
@app.route('/new-disaster-entry', methods = ["POST"]) 
def submit_disaster():
    coord_string = request.form['coordinates']
    


    data = {
        "coordinates" : coord_string,
        "location_name" : request.form['location_name'], 
        "disaster_type" : request.form['disaster_type'],
        "additional-info" : request.form['additional-info'],
    }

    print(data)

    URL = "http://backend-service:5555/new_location"

    r = requests.post(url = URL, data = data)
    print(r.text)
    return redirect("/")

    # return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=8080)