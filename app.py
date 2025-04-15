import streamlit as st
import twitch_api
import pandas as pd

st.set_page_config(page_title="Live Twitch Dashboard", layout="wide")

st.title("🎮 Twitch Live Dashboard")
st.markdown("Live data showing top games and streamers on Twitch")

# Get top games
st.subheader("Top Games on Twitch")
top_games_df = twitch_api.get_top_games()
st.dataframe(top_games_df[['name', 'box_art_url']])

# Game selector
selected_game = st.selectbox("Select a game to see top streamers:", top_games_df['name'])
selected_game_id = top_games_df[top_games_df['name'] == selected_game]['id'].values[0]

# Get top streams for selected game
st.subheader(f"Top Streamers Playing: {selected_game}")
top_streams_df = twitch_api.get_top_streams(game_id=selected_game_id)
st.dataframe(top_streams_df[['user_name', 'title', 'viewer_count', 'started_at']])
