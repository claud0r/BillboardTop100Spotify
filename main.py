"""
    File name:      main.py       
    Author:         Claude Biedermann  
    Date:           11.03.2022            
    Time:           14:33          
"""
import requests
import constants
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/" + date
CLIENT_ID = constants.CLIENT_ID
CLIENT_SECRET = constants.CLIENT_SECRET
REDIRECT_URI = "http://example.com"

# Scraping Billboard 100
response = requests.get(URL)
web_html = response.text
soup = BeautifulSoup(web_html, "html.parser")
song_names_spans = soup.find_all("div", class_="o-chart-results-list-row-container")
song_names = [song.find("h3", id="title-of-a-story").getText().replace('\n','') for song in song_names_spans]

#Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private"))
user_id = sp.current_user()["id"]
print("UserID: " + user_id)

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name="Billboard Top 100 from "+date, public=False)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("Playlist-URL: " + playlist["external_urls"]["spotify"])