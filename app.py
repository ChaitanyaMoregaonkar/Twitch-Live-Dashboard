import streamlit as st
import plotly.express as px
import twitch_api  # This is your helper module for Twitch data

# Configure page settings
st.set_page_config(page_title="Live Twitch Dashboard", layout="wide")
st.title("🎮 Twitch Live Dashboard")
st.markdown("Live data showing top games and top streamers on Twitch.")


top_games_df = twitch_api.get_top_games()

# Select a game to view its streams
selected_game = st.selectbox("Select a game to see top streamers:", top_games_df['name'])
selected_game_id = top_games_df[top_games_df['name'] == selected_game]['id'].values[0]


# Display top streamers for the selected game
st.subheader(f"Top Streamers Playing: {selected_game}")
top_streams_df = twitch_api.get_top_streams(game_id=selected_game_id)
st.dataframe(top_streams_df[['user_name', 'title', 'viewer_count', 'started_at']])

# --- Create a Chart: Aggregated Viewer Count Across Top Games ---
st.subheader("Aggregated Viewer Count Across Top Games")
# Retrieve aggregated viewer data
viewers_data = twitch_api.get_viewers_by_game(top_games_df)

# Create a bar chart using Plotly Express
fig = px.bar(
    viewers_data,
    x='Game',
    y='Total Viewers',
    title='Total Viewers per Top Game',
    labels={'Total Viewers': 'Viewers'},
    template='plotly_white'
)

fig.update_layout(xaxis_tickangle=-45)

# Display the chart in the Streamlit app
st.plotly_chart(fig, use_container_width=True)

# Display the top games table
st.subheader("Top Games on Twitch")
top_games_df = twitch_api.get_top_games()
st.dataframe(top_games_df[['name', 'box_art_url']])




