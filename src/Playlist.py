from Spotify import Spotify
import math
import statistics
import numpy as np
import json
from Models import Features, Track

class PlaylistAPI:

    ROUND_NO = 98
    ROUND_PRE = 99
    ROUND_POST = 100
    ROUND_PRE_POST = 101

    def __init__(self, playlistID, token, length=0):
        self.playlistID = playlistID
        self.spotify = Spotify(token)
        self.length = length
        self.songs = []
        self.features = Features(None)

    def getLength(self):
        if len(self.songs) > 0:
            self.length = len(self.songs)
        else:
            url = f"playlists/{self.playlistID}/tracks"
            selector = {"fields": "total"}

            if self.spotify.query(url, payload=selector):
                self.length = self.spotify.data["total"]

        return self.length

    def getSongs(self):
        if self.length <= 0 or len(self.songs) <= 0:
            self.getLength()
        
        if len(self.songs) > 0:
            return

        iterations = math.ceil(self.length / 100)

        url = f"playlists/{self.playlistID}/tracks"

        tmp = []

        for i in range(iterations):
            selector = {
                "fields": "items(track(name%2Cartists%2Calbum%2Cid))",
                "offset": i * 100,
                "limit": 100
            }
            if self.spotify.query(url, payload=selector):
                for item in self.spotify.data["items"]:
                    tmp.append(Track(item["track"]))

        self.songs = tmp
        return self.songs

    def getFeatures(self):
        if self.length <= 0 or len(self.songs) <= 0:
            self.getSongs()

        if self.songs[0].features != None:
            return

        '''if self.songs[0].features == None:
            print("Jes it was none")

        print("I do it")'''

        iterations = math.ceil(self.length / 100)

        url = "audio-features/"

        songIDs = [song.id for song in self.songs]

        for i in range(iterations):
            from_idx = 100 * i
            to_idx = (100 * (i + 1))#

            localIDs = songIDs[from_idx:to_idx]

            selector = {
                "ids": ",".join(localIDs)
            }

            if self.spotify.query(url, payload=selector):
                for item in self.spotify.data["audio_features"]:
                    features = Features(item)

                    for i, tr in enumerate(self.songs):
                        if tr.id == features.id:
                            self.songs[i].setFeatures(features)
                            break
            else:
                exit(1)

    def _localRound(self, localFeatures, acc=2):
        localFeatures = {
                "danceability": np.around(localFeatures["danceability"], acc),
                "energy": np.round(localFeatures["energy"], acc),
                "loudness": np.round(localFeatures["loudness"], acc),
                "speechiness": np.round(localFeatures["speechiness"], acc),
                "acousticness": np.round(localFeatures["acousticness"], acc),
                "instrumentalness": np.round(localFeatures["instrumentalness"], acc),
                "liveness": np.round(localFeatures["liveness"], acc),
                "valence": np.round(localFeatures["valence"], acc),
                "tempo": np.round(localFeatures["tempo"], acc),
                "duration": np.round(localFeatures["duration"], acc)
            }
        return localFeatures

    def analyse(self, average=statistics.mean, roundStage=ROUND_NO, roundAccuracy=2):

        localFeatures = {
            "danceability": [item.features.danceability for item in self.songs],
            "energy": [item.features.energy for item in self.songs],
            "loudness": [item.features.loudness for item in self.songs],
            "speechiness": [item.features.speechiness for item in self.songs],
            "acousticness": [item.features.acousticness for item in self.songs],
            "instrumentalness": [item.features.instrumentalness for item in self.songs],
            "liveness": [item.features.liveness for item in self.songs],
            "valence": [item.features.valence for item in self.songs],
            "tempo": [item.features.tempo for item in self.songs],
            "duration": [item.features.duration for item in self.songs]
        }

        if roundStage is self.ROUND_PRE or roundStage is self.ROUND_PRE_POST:
            localFeatures = self._localRound(localFeatures, roundAccuracy)
        
        localFeatures = {
            "danceability": average(localFeatures["danceability"]),
            "energy": average(localFeatures["energy"]),
            "loudness": average(localFeatures["loudness"]),
            "speechiness": average(localFeatures["speechiness"]),
            "acousticness": average(localFeatures["acousticness"]),
            "instrumentalness": average(localFeatures["instrumentalness"]),
            "liveness": average(localFeatures["liveness"]),
            "valence": average(localFeatures["valence"]),
            "tempo": average(localFeatures["tempo"]),
            "duration": average(localFeatures["duration"])
        }

        if roundStage is self.ROUND_POST or roundStage is self.ROUND_PRE_POST:
            localFeatures = self._localRound(localFeatures, roundAccuracy)

        self.features = Features(localFeatures)

        return self.features

    def instrumentalOnly(self):
        return self.features.instrumentalness > 0.6

    def speechOnly(self):
        return self.features.speechiness > 0.5