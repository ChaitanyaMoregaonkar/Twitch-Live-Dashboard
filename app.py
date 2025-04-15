import streamlit as st
import twitch_api

# Configure the Streamlit page
st.set_page_config(page_title="Twitch Dashboard", layout="wide")
st.title("Twitch Dashboard")
st.markdown("A basic dashboard that shows **Top Games Streamed** and **Top Streamers** sorted by viewer count. "
            "Select a game to view its specific top streamers.")

# --- Section 1: Top Games Streamed ---
st.subheader("Top Games Streamed")
top_games_df = twitch_api.get_top_games()
if not top_games_df.empty:
    # Show selected columns from the top games data
    st.dataframe(top_games_df[['id', 'name', 'box_art_url']])
else:
    st.write("No top games data available.")

# --- Section 2: Overall Top Streamers by Viewer Count ---
st.subheader("Overall Top Streamers by Viewer Count")
top_streams_df = twitch_api.get_top_streams()
if not top_streams_df.empty:
    st.dataframe(top_streams_df[['user_name', 'game_id', 'viewer_count', 'title']])
else:
    st.write("No stream data available.")

# --- Section 3: Top Streamers for a Selected Game ---
st.subheader("Top Streamers for a Selected Game")
if not top_games_df.empty:
    # Create a dropdown of game names
    game_names = top_games_df['name'].tolist()
    selected_game = st.selectbox("Select a Game", game_names)
    
    # Get the game id for the selected game
    game_id = top_games_df[top_games_df['name'] == selected_game]['id'].iloc[0]
    
    # Retrieve and display top streams for that game
    top_streams_for_game = twitch_api.get_top_streams(game_id=game_id)
    if not top_streams_for_game.empty:
        st.dataframe(top_streams_for_game[['user_name', 'viewer_count', 'title']])
    else:
        st.write("No streams available for the selected game.")
else:
    st.write("No games available to select.")
