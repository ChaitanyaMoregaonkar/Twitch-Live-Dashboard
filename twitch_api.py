import requests
import json
import pandas as pd
from pandas import json_normalize
import streamlit as st

@st.cache_data(ttl=300)
def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': st.secrets["client_id"],
        'client_secret': st.secrets["client_secret"],
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    access_token = response.json()['access_token']
    return access_token

def get_headers():
    access_token = get_access_token()
    return {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': st.secrets["client_id"]
    }

@st.cache_data(ttl=300)
def get_top_games():
    headers = get_headers()
    url = 'https://api.twitch.tv/helix/games/top?first=10'
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    return pd.json_normalize(data)

@st.cache_data(ttl=300)
def get_top_streams(game_id=None):
    headers = get_headers()
    base_url = 'https://api.twitch.tv/helix/streams?first=10'
    if game_id:
        base_url += f"&game_id={game_id}"
    response = requests.get(base_url, headers=headers)
    data = response.json()['data']
    return pd.json_normalize(data)
