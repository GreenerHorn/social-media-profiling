import flask
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import json
import DatabaseHandler
import Details
import Log
from Parser import Parser
from Recommendation import Recommender

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return "Hello"


@app.route('/postData', methods=['POST'])
def postData():
    try:
        name = request.json["name"]
        email = request.json["email"]
        phone = request.json["mob_no"]
    except Exception as e:
        Log.log("Error" + str(e))
        return json.dumps(Details.Detail().__dict__)
    ans = Parser.parse(name, email, phone)
    Log.log("ans  = ",ans)
    if '_id' in ans:
        ans.pop('_id', None)
    return json.dumps(ans)

@app.route('/getData', methods=['POST'])
def getData():
    try:
        email = request.json["email"]
    except Exception as e:
        Log.log("Error" + str(e))
        return json.dumps(Details.Detail().__dict__)
    ans = DatabaseHandler.DataBaseHandler().get_data_with_email(email)
    x= jsonify(ans.__dict__)
    print(x)
    print(ans.__dict__)
    return jsonify(ans.__dict__)


@app.route('/getRecommendation', methods=['POST'])
def getRecommendation():
    email = request.json["email"]
    data = DatabaseHandler.DataBaseHandler().get_data_with_email(email)
    recommend = Recommender.get_recommendation(data)
    return jsonify(recommend)


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
