import requests
from bs4 import BeautifulSoup
import re
import warnings
import pandas as pd
import os

warnings.filterwarnings('ignore')


artist_urls=["https://www.lyrics.com/artist/Simon-%26-Garfunkel/5431", \
            "https://www.lyrics.com/artist/Michael-Jackson/4576" \
            "https://www.lyrics.com/artist/Rihanna/704560",
            "https://www.lyrics.com/artist/Eminem/347307", \
            "https://www.lyrics.com/artist/Madonna/64565", \
            "https://www.lyrics.com/artist/Tupac-Shakur/557759", \
            "https://www.lyrics.com/artist/Mumford-%26-Sons/1570809", \
            "https://www.lyrics.com/artist/The-Tallest-Man-on-Earth/865422", \
            "https://www.lyrics.com/artist/Sam-Smith/2213398", \
            "https://www.lyrics.com/artist/Whitney-Houston/4519", \
            "https://www.lyrics.com/artist/The-Darkness/572345", \
            "https://www.lyrics.com/artist/Bob-Dylan/4147", \
            "https://www.lyrics.com/artist/Bon-Iver/991558", \
            "https://www.lyrics.com/artist/Joni-Mitchell/4930", \
            "https://www.lyrics.com/artist/Backstreet-Boys/199819", \
            "https://www.lyrics.com/artist/Dru-Hill/198612", \
            "https://www.lyrics.com/artist/Jay-Z/195154", \
            "https://www.lyrics.com/artist/Lady-Gaga/1055684", \
            "https://www.lyrics.com/artist/Amy-Winehouse/612371", \
            "https://www.lyrics.com/artist/Adele/861756"]


artists = []
for url in artist_urls:
    url_artistPage = url
    artist = url.split("/")[-2]
    artists.append(artist)
    
    artistPage = requests.get(url_artistPage)

    with open(f"Data/Webscraping/{artist}_listOfSongs.txt", "w") as f:
        f.write(artistPage.text)

for artist in artists:
    file = open(f"Data/Webscraping/{artist}_listOfSongs.txt", "r")
    text = file.read()
    pattern = 'href\=\"\/lyric([^\>]+)\"'
    songUrls = re.findall(pattern,text)

    count = 0
    for url in songUrls:
        song_url = "https://www.lyrics.com/lyric" + url

        songPage = requests.get(song_url)
        songSoup = BeautifulSoup(songPage.text)
        songBody = songSoup.find(id = "lyric-body-text").text
        songTitle = songSoup.find(id = "lyric-title-text").text
        songTitle = songTitle.replace("/","").replace("\"", "")
        
        with open(f"Data/Webscraping/song_lyrics/{artist}_{songTitle}.txt", "w") as f:
            f.write(songBody)
            
            count += 1
            print(artist, songTitle)
            print("count", count)
         
        


    