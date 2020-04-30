from Util import Serializeable

class Artist(Serializeable):
    def __init__(self, artist):
        self.id = artist["id"]
        self.name = artist["name"]

class Album(Serializeable):
    def __init__(self, album):
        self.id = album["id"]
        self.images = Images(album["images"])
        self.name = album["name"]

class Image(Serializeable):
    def __init__(self, image):
        self.url = image["url"]
        self.height = image["height"]
        self.width =  image["width"]

class Images(Serializeable):
    def __init__(self, images):
        if "normalImage" in images:
            '''self.smallImage = Image(images["smallImage"])
            self.midImage = Image(images["midImage"])'''
            self.normalImage = Image(images["normalImage"])
        else:
            '''self.smallImage = Image(images[2])
            self.midImage = Image(images[1])'''
            self.normalImage = Image(images[0])

class Track(Serializeable):
    def __init__(self, track):
        self.id = track["id"]
        self.name = track["name"]
        self.artists = [Artist(artist) for artist in track["artists"]]
        self.album = Album(track["album"])
        if "features" in track:
            if track["features"] != None:
                self.features = Features(track["features"])
            else:
                self.features = None
        else:
            self.features = None

    def setFeatures(self, feats):
        self.features = feats

class Features(Serializeable):
    def __init__(self, features):
        if features == None:
            features = {
                "danceability": 0.0,
                "energy": 0.0,
                "loudness": 0.0,
                "speechiness": 0.0,
                "acousticness": 0.0,
                "instrumentalness": 0.0,
                "liveness": 0.0,
                "valence": 0.0,
                "tempo": 0.0,
                "duration_ms": 0
            }

        self.danceability = float(features["danceability"])
        self.energy = float(features["energy"])
        self.loudness = float(features["loudness"])
        self.speechiness = float(features["speechiness"])
        self.acousticness = float(features["acousticness"])
        self.instrumentalness = float(features["instrumentalness"])
        self.liveness = float(features["liveness"])
        self.valence = float(features["valence"])
        self.tempo = float(features["tempo"])
        if "duration" in features:
            self.duration = int(features["duration"])
        else:
            self.duration = int(features["duration_ms"])

        if "id" in features:
            self.id = features["id"]