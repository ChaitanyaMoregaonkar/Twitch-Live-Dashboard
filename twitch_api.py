import requests
import pandas as pd
from pandas import json_normalize
import streamlit as st

@st.cache_data(ttl=300)
def get_access_token():
    """
    Request and cache the Twitch OAuth access token.
    """
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': st.secrets["client_id"],
        'client_secret': st.secrets["client_secret"],
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    token_json = response.json()
    return token_json['access_token']

def get_headers():
    """
    Build the headers for Twitch API requests.
    """
    access_token = get_access_token()
    return {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': st.secrets["client_id"]
    }

@st.cache_data(ttl=300)
def get_top_games():
    """
    Retrieve the top 10 games being streamed on Twitch.
    """
    headers = get_headers()
    url = 'https://api.twitch.tv/helix/games/top?first=10'
    response = requests.get(url, headers=headers)
    data = response.json().get('data', [])
    return pd.json_normalize(data)

@st.cache_data(ttl=300)
def get_top_streams(game_id=None):
    """
    Retrieve the top streams. If a game_id is specified,
    only return streams for that game.
    """
    headers = get_headers()
    base_url = 'https://api.twitch.tv/helix/streams?first=100'
    if game_id:
        base_url += f'&game_id={game_id}'
    response = requests.get(base_url, headers=headers)
    data = response.json().get('data', [])
    df = pd.json_normalize(data)
    if not df.empty:
        df['viewer_count'] = pd.to_numeric(df['viewer_count'], errors='coerce')
        # Sort streams by viewer count in descending order
        df.sort_values(by='viewer_count', ascending=False, inplace=True)
    return df
