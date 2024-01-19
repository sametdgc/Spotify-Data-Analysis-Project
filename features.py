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

client_id = os.getenv("CLIENT_ID4")
client_secret = os.getenv("CLIENT_SECRET4")
df_loaded = pd.read_csv('spotify_final.csv')




def get_auth_header(token):
    headers = {"Authorization": "Bearer " + token}
    return headers



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

# def get_audio_features(track_id, token):
#     url = f"https://api.spotify.com/v1/audio-features/{track_id}"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     return json.loads(result.content)

def get_audio_features(track_id, token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)

    if result.status_code == 200:
        audio_features = json.loads(result.content)
        return audio_features
    else:
        print(f"Failed to retrieve audio features for track ID: {track_id}")
        return None

# def add_audio_features_columns(row):
#     track_id = row["track_id"]
#     if track_id:
#         audio_features = get_audio_features(track_id, token)
#         if audio_features:
#             # Extract relevant audio features and add as new columns
#             row["danceability"] = audio_features.get("danceability", None)
#             row["energy"] = audio_features.get("energy", None)
#             row["valence"] = audio_features.get("valence", None)
#             row["tempo"] = audio_features.get("tempo", None)
#             row["duration_ms"] = audio_features.get("duration_ms", None)
#         else:
#             row["danceability"] = None
#             row["energy"] = None
#             row["valence"] = None
#             row["tempo"] = None
#             row["duration_ms"] = None
#     return row


# def add_audio_features_columns(row):
#     track_id = row["track_id"]
#     if track_id:
#         # Check if the columns are empty before retrieving and adding audio features
#         if pd.isnull(row["danceability"]) or pd.isnull(row["energy"]) or pd.isnull(row["valence"]) or pd.isnull(row["tempo"]) or pd.isnull(row["duration_ms"]):
#             audio_features = get_audio_features(track_id, token)
#             if audio_features:
#                 # Extract relevant audio features and add as new columns
#                 row["danceability"] = audio_features.get("danceability", None)
#                 row["energy"] = audio_features.get("energy", None)
#                 row["valence"] = audio_features.get("valence", None)
#                 row["tempo"] = audio_features.get("tempo", None)
#                 row["duration_ms"] = audio_features.get("duration_ms", None)
#             else:
#                 row["danceability"] = None
#                 row["energy"] = None
#                 row["valence"] = None
#                 row["tempo"] = None
#                 row["duration_ms"] = None
#     return row
# Apply the function to each row in the DataFrame
def add_audio_features_columns(row):
    if row.name >= 2000:
        track_id = row["track_id"]
        if track_id:
            audio_features = get_audio_features(track_id, token)
            if audio_features:
                # Extract relevant audio features and add as new columns
                row["danceability"] = audio_features.get("danceability", None)
                row["energy"] = audio_features.get("energy", None)
                row["valence"] = audio_features.get("valence", None)
                row["tempo"] = audio_features.get("tempo", None)
                row["duration_ms"] = audio_features.get("duration_ms", None)
            else:
                row["danceability"] = None
                row["energy"] = None
                row["valence"] = None
                row["tempo"] = None
                row["duration_ms"] = None
    return row
pbar = tqdm(total=len(df_loaded))

df_loaded = df_loaded.apply(add_audio_features_columns, axis=1)


pbar.close()

print(df_loaded.head())

df_loaded.to_csv("spotify_final2.csv", index=False)

