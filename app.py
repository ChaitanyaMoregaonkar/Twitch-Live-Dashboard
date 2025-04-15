import streamlit as st
import plotly.express as px
import twitch_api  # Ensure that twitch_api.py is in the same directory

# Configure page settings
st.set_page_config(page_title="Live Twitch Dashboard", layout="wide")
st.title("🎮 Twitch Live Dashboard")
st.markdown("This dashboard shows the Top Games (based on viewer counts) and displays the Top Streamers for the selected game.")

# --- Display Bar Chart for Top Games by Total Viewers ---
st.subheader("Top Games by Total Viewers")
# Fetch top games data
top_games_df = twitch_api.get_top_games()
viewers_data = twitch_api.get_viewers_by_game(top_games_df)

# Create a bar chart using Plotly Express
fig = px.bar(
    viewers_data,
    x='Game',
    y='Total Viewers',
    title='Total Viewers by Top Game',
    labels={'Total Viewers': 'Viewers'},
    template='plotly_white'
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# --- Interactive Component: Select a Game to See Top Streamers ---
st.subheader("Top Streamers for Selected Game")
# Select a game from the bar chart data
selected_game = st.selectbox("Select a game:", viewers_data['Game'])
# Match the game name to retrieve its game ID from the top_games_df
selected_game_id = top_games_df[top_games_df['name'] == selected_game]['id'].values[0]

# Fetch top streams for the selected game
top_streams_df = twitch_api.get_top_streams(game_id=selected_game_id)
if not top_streams_df.empty:
    st.dataframe(top_streams_df[['user_name', 'title', 'viewer_count', 'started_at']])
else:
    st.write("No live streams available for this game at the moment.")
