import json
import datetime
#from flask_lambda import FlaskLambda
#from flask import request
import requests


#app = FlaskLambda(__name__)


'''
@app.route('/')
def handler():
    data = {
        'output': 'Hello World 2',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return json_response(data)

@app.route('/students', methods=['GET', 'POST'])
def put_list_students():
    return json_response({"message": "from students"})'''


def handler(event, context):
    print(event)
    print(context)
    data = event
    # token = request.headers.get("Token")

    #if token == None:
    #    return json_response({"error": "No token provided"}, response_code=401)

    #data = {"token": token}

    #if id == None:
        # From Databse?
        #data = {"message": "from db"}
        #id = "37i9dQZF1DZ06evO2dYtbO"

    '''
    playlist = PlaylistAPI(id, token)

    if request.method == "GET":
        # Analyse and get Songs
        playlist.getFeatures()
        data = {"message": "get feaatures"}
        data = playlist.analyse(Util.better_mean, roundStage=PlaylistAPI.ROUND_POST, roundAccuracy=3)
        pass
    elif request.method == "POST":
        # Playlist data should be given
        dictin = request.get_json()
        test = dictin["items"]
        data = {"message": f"from post with data {test}"}'''

    return json_response(data)

def json_response(data, response_code=200):
    return {
        'statusCode': response_code,
        'body': json.dumps(data),
        'headers': {'Content-Type': 'application/json'}
    }