from Spotify import Spotify
from Playlist import PlaylistAPI
from Util import better_mean, list2json, json2obj
import statistics
import json
import time
from Models import Track
from Genius import Genius
beg = time.time()

token = "BQBPEX_Zo3Eu1sGfSOe23PGUxt9bGkbOLxH95mrjcyc3Cj8fwqEE4EuGVi3G8Neo7mOEXCLIeNCOQXm0MPAIvYm6YU7UzSJqiF6XYzlgSGbkjhOl1NtkfmqWA7cum2CnYOeth-P3_9RbBOORhQxucYIeI7BT-Z3jsDY5qiqApRyICifRzuTYg7hSZqIoR2ssYUxKJuITYmBUzJCB2S4MyLgQbh4swmaNS6MO69_tjbgFRWUTZOIVGSp4c858pJGG5cmuHeFeH-_dqV85Zkht"

playlist = PlaylistAPI(playlistID="37i9dQZF1DZ06evO2dYtbO", token=token)

try:
    with open("playlist_dump_features.json", "r") as f:
        playlist.songs = [Track(t) for t in json2obj(f.read())]
except:
    print("File not loaded")
    pass

print("Post LOAD:", time.time() - beg)

playlist.getSongs()

print("Post getSongs():", time.time() - beg)

'''spot = Spotify(token)
if not spot.query("me/playlists"):
    print(spot.status)
    exit(1)

r = spot.data

print("\n".join([(f"Name: {item['name']} ID: {item['id']}") for item in r["items"]]))'''

with open("playlist_no_feats.json", "w") as f:
    f.write(list2json(playlist.songs))
    f.close()

print("Post SAVE:", time.time() - beg)

playlist.getFeatures()

#print(playlist.singleFeatures[:10])

print("Post getFeatures():", time.time() - beg)

with open("playlist_dump_features.json", "w") as f:
    f.write(list2json(playlist.songs))
    f.close()

print("Post Save:", time.time() - beg)

playlist.analyse(average=better_mean, roundStage=PlaylistAPI.ROUND_NO, roundAccuracy=4)
print("Values:", playlist.features.toJSON())

print("Post analyse():", time.time() - beg)

gen = Genius("7svL8WRo-kLg4COkIuyrpNAxQHrk-maOFQ6tIXKT51wwh-eJ8Bda0AP9YvFbxgoI")
url = gen.getSongURL("'Til I Collapse", "Eminem")
lyr = gen.get_lyrics_from_url(url)
print(lyr)