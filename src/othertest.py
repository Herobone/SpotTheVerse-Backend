from LambdaProcessor import Processor
import json
from Playlist import PlaylistAPI
import Util

proc = Processor()

@proc.register("/analyse/{id}")
@proc.register("/analyse")
def test2(request: 'Request', id=None):

    token = request.headers.get("Token")

    if token == None:
        return json_response({"error": "No token provided"}, response_code=401)

    data = {"token": token}

    if id == None:
        # From Databse?
        data = {"message": "from db"}
        id = "37i9dQZF1DZ06evO2dYtbO"

    
    playlist = PlaylistAPI(id, token)

    if request.method == "GET":
        # Analyse and get Songs
        playlist.getFeatures()
        data = {"message": "get features"}
        data = playlist.analyse(Util.better_mean, roundStage=PlaylistAPI.ROUND_POST, roundAccuracy=3).toJSON()
        pass
    elif request.method == "POST":
        # Playlist data should be given
        dictin = request.get_json()
        test = dictin["items"]
        data = {"message": f"from post with data {test}"}

    return json_response(data)

@proc.register("/")
def test3(request):
    print("Test 3")
    return standard()

print(proc.REGS)

def standard():
    return json_response({"data": "standard"})

def json_response(data, response_code=200):
    return {
        'statusCode': response_code,
        'body': json.dumps(data),
        'headers': {'Content-Type': 'application/json'}
    }