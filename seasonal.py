from requests import post, get
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os 
import base64
import json
from unidecode import unidecode
from tqdm import tqdm

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print("CLIENT_ID:", client_id)
# print("CLIENT_SECRET:", client_secret)
def get_audio_features(track_id, token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return json.loads(result.content)

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_string_bytes = auth_string.encode("utf-8")
    auth_string_base64 = str(base64.b64encode(auth_string_bytes), "utf-8")

    t_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_string_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(t_url, headers=headers, data=data)
    json_result = json.loads(result.content) 
    token = json_result["access_token"]
    return token

token = get_token()


def get_auth_header(token):
    headers = {"Authorization": "Bearer " + token}
    return headers


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    search_url = url + "?" + query
    result = get(search_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if (len(json_result) == 0):
        print("No artist found")
        return None
    return json_result[0]

def search_for_genres(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    search_url = url + "?" + query
    result = get(search_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if (len(json_result) == 0):
        print("No artist found")
        return None
    return json_result[0]["genres"]

def get_songs(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

#result = search_for_artist(token, "Büyük Ev Ablukada")
#songs = get_songs(token, result["id"])
def search_for_tracks(token, track_name, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={track_name} {artist_name}&type=track&limit=1"
    search_url = url + "?" + query
    result = get(search_url, headers=headers)
    
    try:
        track_id = json.loads(result.content)["tracks"]["items"][0]["id"]
        return track_id
    except (KeyError, IndexError):
        print("No track found")
        return None

def get_audio_features(track_id, token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return json.loads(result.content)
def print_song(song):
    # Encode the song name to the console encoding
    ascii_song_name = unidecode(song['name'])
    print(f"{song['track_number']}. {ascii_song_name}")


art = search_for_genres(token, "Büyük Ev Ablukada")

print("ARTIST:", art)
# ...

def get_season(month):
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [9, 10, 11]:
        return 'fall'
    else:
        return 'unknown'
# print("RESULT:", result["name"])
# print("artist id:", result["id"])


file_paths = ["StreamingHistory0.json", "StreamingHistory1.json", "StreamingHistory2.json"]

# Initialize an empty list to store data from all files
all_data = []

# Loop through each file and load the data into the list
for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        all_data.extend(data)

# Create a pandas DataFrame from the combined data
df = pd.DataFrame(all_data)
# Apply unidecode to "artistName" and "trackName" columns
df["artistName"] = df["artistName"].apply(unidecode)
df["trackName"] = df["trackName"].apply(unidecode)

# Extract the season from the "endTime" column
df["endTime"] = pd.to_datetime(df["endTime"])
df["season"] = df["endTime"].dt.month.apply(get_season)

# Group by "artistName", "trackName", and "season" and calculate the total "msPlayed"
df_grouped = df.groupby(["artistName", "trackName", "season"])["msPlayed"].sum().reset_index()

# Pivot the DataFrame to have separate columns for each season
df_pivoted = df_grouped.pivot_table(index=["artistName", "trackName"], columns="season", values="msPlayed", fill_value=0).reset_index()

# Display the resulting DataFrame
#print(df_pivoted.head())



def get_genres_for_row(row):
    artist_name = row["artistName"]
    return search_for_genres(token, artist_name)

# Apply the function to each row to get genres
tqdm.pandas()  # Enable progress bar for pandas apply
df_pivoted["genres"] = df_pivoted.progress_apply(get_genres_for_row, axis=1)

# Display the resulting DataFrame
print(df_pivoted.head())
specific_song = df_pivoted.loc[df_pivoted["trackName"] == "Mykonos"]
print(specific_song)
df_pivoted['genres'] = df_pivoted['genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)



def search_for_tracks_and_features(token, track_name, artist_name):
    track_id = search_for_tracks(token, track_name, artist_name)
    if track_id:
        audio_features = get_audio_features(track_id, token)
        return track_id, audio_features
    return None, None

df_pivoted[["trackID", "audio_features"]] = df_pivoted.apply(lambda row: search_for_tracks_and_features(token, row["trackName"], row["artistName"]), axis=1).apply(pd.Series)

df_pivoted["danceability"] = df_pivoted["audio_features"].apply(lambda x: x["danceability"] if x else None)
df_pivoted["energy"] = df_pivoted["audio_features"].apply(lambda x: x["energy"] if x else None)
df_pivoted["valence"] = df_pivoted["audio_features"].apply(lambda x: x["valence"] if x else None)
df_pivoted["tempo"] = df_pivoted["audio_features"].apply(lambda x: x["tempo"] if x else None)
df_pivoted["duration_ms"] = df_pivoted["audio_features"].apply(lambda x: x["duration_ms"] if x else None)



df_pivoted = df_pivoted.drop(columns=["audio_features"])

print(df_pivoted.head())

df_pivoted.to_csv("spotify_data_features.csv", index=False)
