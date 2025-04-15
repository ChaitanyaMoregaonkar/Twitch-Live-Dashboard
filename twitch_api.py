import requests
import pandas as pd
from pandas import json_normalize
import streamlit as st

@st.cache_data(ttl=300)
def get_access_token():
    """
    Request and cache the Twitch OAuth access token.
    """
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": st.secrets["client_id"],
        "client_secret": st.secrets["client_secret"],
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    access_token = response.json()["access_token"]
    return access_token

def get_headers():
    """
    Create the headers required for Twitch API requests.
    """
    access_token = get_access_token()
    return {
        "Authorization": f"Bearer {access_token}",
        "Client-ID": st.secrets["client_id"]
    }

@st.cache_data(ttl=300)
def get_top_games():
    """
    Retrieve the top 10 games from Twitch.
    """
    headers = get_headers()
    url = "https://api.twitch.tv/helix/games/top?first=10"
    response = requests.get(url, headers=headers)
    data = response.json()["data"]
    return pd.json_normalize(data)

@st.cache_data(ttl=300)
def get_top_streams(game_id=None):
    """
    Retrieve the top 10 streams. If a game_id is provided, filter streams for that game.
