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
    access_token = response.json()['access_token']
    return access_token

def get_headers():
    """
    Create headers required for Twitch API requests.
    """
    access_token = get_access_token()
    return {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': st.secrets["client_id"]
    }

@st.cache_data(ttl=300)
def get_top_games():
    """
    Retrieve the top 10 games from Twitch.
    """
    headers = get_headers()
    url = 'https://api.twitch.tv/helix/games/top?first=10'
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    return pd.json_normalize(data)

@st.cache_data(ttl=300)
def get_top_streams(game_id=None):
    """
    Retrieve the top 10 streams.
    If a game_id is provided, filter streams for that game.
    """
    headers = get_headers()
    base_url = 'https://api.twitch.tv/helix/streams?first=10'
    if game_id:
        base_url += f"&game_id={game_id}"
    response = requests.get(base_url, headers=headers)
    data = response.json()['data']
    return pd.json_normalize(data)

@st.cache_data(ttl=300)
def get_viewers_by_game(top_games_df):
    """
    For each game in the top games DataFrame, fetch the top streams
    and sum up the viewer_count. Returns a DataFrame with each game's total viewers.
    """
    game_names = []
    total_viewers = []
    
    for index, row in top_games_df.iterrows():
        game_id = row.get('id')
        game_name = row.get('name')
        streams_df = get_top_streams(game_id=game_id)
        if streams_df.empty:
            viewers_sum = 0
        else:
            # Convert viewer_count to numeric in case it is not already
            streams_df['viewer_count'] = pd.to_numeric(streams_df['viewer_count'], errors='coerce')
            viewers_sum = streams_df['viewer_count'].sum()
        game_names.append(game_name)
        total_viewers.append(viewers_sum)
    
    df_viewers = pd.DataFrame({
        'Game': game_names,
        'Total Viewers': total_viewers
    })
    
    return df_viewers.sort_values(by='Total Viewers', ascending=False)
