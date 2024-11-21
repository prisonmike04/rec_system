import streamlit as st
import json
import pandas as pd
import plotly.express as px
import random
from PIL import Image

# Load the JSON dataset (ensure the file is in the same directory or update the path)
DATA_FILE = "recommendation_dataset.json"

with open(DATA_FILE, "r") as file:
    data = json.load(file)

# Convert the JSON data to a pandas DataFrame for easier processing
user_data = pd.json_normalize(data["users"])

# Function to get user details
def get_user_recommendations(user_id):
    user = next((u for u in data["users"] if u["user_id"] == user_id), None)
    if user:
        # Ensure that watch_time exists and is a dictionary
        watch_time = pd.DataFrame(
            list(user["watch_time"].items()), columns=["Day", "Hours"]
        ) if isinstance(user["watch_time"], dict) else pd.DataFrame(columns=["Day", "Hours"])
        return user, watch_time
    return None, None

# Streamlit UI
# Center and display logo (check if file exists)
try:
    image = Image.open("jio.png")  # Make sure the file exists in your directory
    st.image(image, caption="Welcome to Jio Cinemas", width=150)
except FileNotFoundError:
    st.error("Logo file 'jio.png' not found!")

# Title and Description
st.title("📺 Personalized Recommendation System")
st.markdown("Welcome to the recommendation system! Enter your user ID to get personalized recommendations and explore detailed analytics.")

# User ID input
user_id = st.number_input("Enter your User ID :", min_value=1, max_value=25, step=1)

# Display user details and recommendations
if st.button("Get Recommendations"):
    user, watch_time = get_user_recommendations(user_id)
    if user:
        st.header(f"Hello, User {user_id}!")
        st.subheader("Your Recommended Series:")
        st.image(user["image_url"], caption=user["series"], width=300)
        st.write(f"**Series:** {user['series']}")
        st.write(f"**Genre:** {user['genre']}")
        st.write(f"**Description:** {user['description']}")
        st.write(f"**Preferred Genres:** {user['preferred_genres']}")

        # Watch Time Analysis (simulated for now)
        if not watch_time.empty:
            st.subheader("Your Weekly Watch Time")
            fig = px.bar(watch_time, x="Day", y="Hours", title="Weekly Watch Time", labels={"Hours": "Hours Watched"})
            st.plotly_chart(fig)
        else:
            st.write("No watch time data available.")
    else:
        st.error("User not found! Please check the User ID.")

# Add a dynamic dashboard for overall analytics
st.markdown("---")
st.header("📊 Overall User Analytics")

# Interactive filtering for analytics
st.subheader("Filters for Analytics")
filter_genre = st.selectbox("Select a Genre to Filter Analytics:", options=["All"] + user_data["preferred_genres"].explode().unique().tolist(), index=0)

# Filter data based on the selected genre
if filter_genre != "All":
    filtered_data = user_data[user_data["preferred_genres"].apply(lambda x: filter_genre in x if isinstance(x, list) else False)]
else:
    filtered_data = user_data

# Pie Chart: Preferred Genres Distribution
st.subheader("Preferred Genres Distribution")
# Ensure that the preferred_genres field is a list and handle any missing/empty values
all_genres = pd.DataFrame(filtered_data["preferred_genres"].dropna().apply(lambda x: x if isinstance(x, list) else [] ).explode(), columns=["Genre"])

if not all_genres.empty:
    genre_counts = all_genres["Genre"].value_counts().reset_index()
    genre_counts.columns = ["Genre", "Count"]
    fig_genres = px.pie(genre_counts, names="Genre", values="Count", title="Preferred Genres Distribution")
    st.plotly_chart(fig_genres)
else:
    st.write("No genre data available to display.")

# Bar Chart: Most Watched Series
st.subheader("Most Watched Series")
series_counts = filtered_data["series"].value_counts().reset_index()
series_counts.columns = ["Series", "Count"]
fig_series = px.bar(series_counts, x="Series", y="Count", title="Most Watched Series", color="Series")
st.plotly_chart(fig_series)

# Line Chart: Fake Average Weekly Watch Time (Randomized Data for Demo)
st.subheader("Average Weekly Watch Time")

# Generate fake data for average weekly watch time
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
fake_data = {
    "Day": days,
    "Average Hours": [random.randint(1, 20) for _ in days]  # Random values between 1 and 5
}

# Create a DataFrame from the fake data
weekly_watch_time = pd.DataFrame(fake_data)

# Plot the random line chart
fig_watch = px.line(weekly_watch_time, x="Day", y="Average Hours", title=" Average Weekly Watch Time")
st.plotly_chart(fig_watch)

# Manually added fake summary statistics
st.markdown("### Summary Statistics")
st.write("**Total Users:** 22000")  # Fake total user count
st.write("**Total Series Watched:** 1040")  # Fake total series count
st.write("**Top Genre:** Action")  # Fake top genre
st.write("**Highest Watch Time Day:** Friday")  # Fake highest watch time day
