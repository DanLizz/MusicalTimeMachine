from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Scraping Billboard for top songs on a particular date

date = input("Which year do you want to travel to? Type the date in this format YYY-MM-DD:")

URL = "https://www.billboard.com/charts/hot-100/"+date
response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

best_songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
for song in best_songs:
    print(song.getText())

#Spotify authentication

CLIENT_ID = Your_Client_Id
CLIENT_SECRET = Your_Client_Secret

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

#Searching spotify for top songs
song_uris = []
year = date.split("-")[0]

for song in best_songs:
    song = song.getText()
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} does not exist in Spotify. Skipped")

#Create a new private playlist in Spotify

playlist = sp.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False)
print(playlist)


#Add songs to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)