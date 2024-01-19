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

client_id = os.getenv("CLIENT_ID2")
client_secret = os.getenv("CLIENT_SECRET2")
df_loaded = pd.read_csv('spotify_data2.csv')


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

def get_audio_features(track_id, token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return json.loads(result.content)

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

def search_for_tracks(token, track_name):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"q={track_name}&type=track&limit=1"
    search_url = url + "?" + query
    result = get(search_url, headers=headers)

    json_result = json.loads(result.content).get("tracks", {}).get("items", [])
    
    if len(json_result) == 0:
        print("No track found")
        return None
    
    return json_result[0].get('id', None)

def add_track_id_column(row):
    track_id = search_for_tracks(token, row["trackName"] + row["artistName"])
    row["track_id"] = track_id
    return row

df_loaded = df_loaded.apply(add_track_id_column, axis=1)

print(df_loaded.head())

df_loaded.to_csv("spotify_data_IDs_corrected.csv", index=False)

