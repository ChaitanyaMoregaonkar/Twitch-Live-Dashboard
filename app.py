import streamlit as st
import plotly.express as px
import twitch_api
from streamlit_plotly_events import plotly_events

# Configure the page settings
st.set_page_config(page_title="Twitch Dashboard", layout="wide")
st.title("🎮 Twitch Dashboard")
st.markdown("A basic dashboard showing top games (by total viewers) and, upon selection, their top streamers.")

# Load the top games DataFrame from Twitch API
top_games_df = twitch_api.get_top_games()
# Aggregate viewer counts for each game
viewers_data = twitch_api.get_viewers_by_game(top_games_df)

# Create a bar chart to visualize total viewers per game
fig = px.bar(
    viewers_data,
    x="Game",
    y="Total Viewers",
    title="Top Games by Total Viewers",
    labels={"Total Viewers": "Viewer Count"},
    template="plotly_white"
)
fig.update_layout(xaxis_tickangle=-45)

# Display the interactive bar chart and capture click events
st.subheader("Click on a bar to view top streamers for that game")
selected_points = plotly_events(fig, click_event=True, hover_event=False)

# Determine the selected game based on the click event, otherwise default to the top game
if selected_points:
    selected_game = selected_points[0]["x"]
    st.write(f"**Selected Game:** {selected_game}")
else:
    selected_game = viewers_data.iloc[0]["Game"]
    st.write(f"**Default Game (no selection):** {selected_game}")

# Look up the game_id for the selected game
game_row = top_games_df[top_games_df["name"] == selected_game]
if not game_row.empty:
    selected_game_id = game_row["id"].iloc[0]
    # Retrieve and display the top streams for the selected game
    st.subheader(f"Top Streamers for {selected_game}")
    streams_df = twitch_api.get_top_streams(game_id=selected_game_id)
    if streams_df.empty:
        st.write("No active streams for this game.")
    else:
        st.dataframe(streams_df[["user_name", "title", "viewer_count", "started_at"]])
else:
    st.write("Selected game not found in the data.")
