import json
from collections import namedtuple
import statistics
import requests
from enum import Enum

def _json_object_hook(d):
        return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data)

def list2json(data):
    return json.dumps(data, default=lambda o: o.__dict__, 
            sort_keys=True, indent=None)

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Serializeable:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=None)

class API:
    def __init__(self, baseUrl, token):
        self.baseUrl = baseUrl
        self.token = token

    def query(self, url, payload=None):
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(
            f"{self.baseUrl}{url}", params=payload, headers=headers)

        if r.status_code == 200:
            self.status = Status.REQUEST_OK
            self.data =  r.json()
            return True

        elif r.status_code == 401:
            self.status = Status.TOKEN_INVALID
            self.data = None
            return False

        elif r.status_code == 404:
            self.status = Status.NOT_FOUND
            self.data = None
            return False

        elif r.status_code == 429:
            self.status = Status.THROTTLED
            self.data = None
            return False

        else:
            self.status = Status.OTHER_ERROR
            self.data = None
            return False

class Status(Enum):
    REQUEST_OK = 1
    TOKEN_INVALID = 2
    NOT_FOUND = 3
    THROTTLED = 4
    OTHER_ERROR = 5

def better_mean(data):
    try:
        return statistics.harmonic_mean(data)
    except:
        return statistics.mean(data)