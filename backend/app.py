from flask import Flask

app = Flask(__name__)





@app.route('/test', methods = ["GET"]) 
def test():

    return { "result" : "testing OK" }
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5555)