import json
import datetime
from flask_lambda import FlaskLambda
from flask import request


app = FlaskLambda(__name__)



@app.route('/')
def handler():
    data = {
        'output': 'Hello World 2',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return json_response(data)

@app.route('/students', methods=['GET', 'POST'])
def put_list_students():
    return json_response({"message": "from students"})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}