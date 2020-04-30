import requests
from Util import API

class Spotify(API):

    def __init__(self, token):
        super().__init__("https://api.spotify.com/v1/", token)

