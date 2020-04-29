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
    data = {
        'output': 'Hello World',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}