from bs4 import BeautifulSoup
import re
import requests
from Util import API

class Genius(API):

    def __init__(self, token):
        super().__init__("https://api.genius.com/", token)

    def search(self, search):
        return self.query("search", payload={"q": search})

    def getSongURL(self, name, artist):
        track = name.split("-")[0]
        track = re.sub('(\(.*?\))*', '', track)
        track = re.sub('(\[.*?\])*', '', track).strip()
        if not self.search(f"{track} {artist}"):
            print(self.status)
            exit(1)
        for hit in self.data["response"]["hits"]:
            res = hit["result"]
            if res["primary_artist"]["name"] == artist:
                return res["url"]

    def get_lyrics_from_url(self, url):
        page = requests.get(url)
        if page.status_code == 404:
            return None

        # Scrape the song lyrics from the HTML
        html = BeautifulSoup(page.text, "html.parser")
        div = html.find("div", class_="lyrics")
        if not div:
            return None # Sometimes the lyrics section isn't found

        # Scrape lyrics if proper section was found on page
        lyrics = div.get_text()
        lyrics = re.sub('(\[.*?\])*', '', lyrics) # [Chorus], [Verse] and so on removed
        lyrics = re.sub('\n{2}', '', lyrics)  # Gaps between verses
        return lyrics.strip("\n").split("\n")