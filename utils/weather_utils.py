import streamlit as st
from datetime import datetime
import requests

# Set up the API key and dam URLs
API_KEY = "9B3WL9NM69WZMS3G4AY7ZDALZ"
dam_urls = {
    "mettur": f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/mettur",
    "kabini": f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Beechanahalli",
    "krs": f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/krishna%20raja%20sagar"
}

dam_name = "mettur"  # Hardcoded dam name

# Fetch weather data from the API
def fetch_weather_features(date, dam_name):
    try:
        url = f"{dam_urls[dam_name]}/{date}?key={API_KEY}"
        response = requests.get(url)
        data = response.json()['days'][0]
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Map weather features to your application model
def map_weather_features(day_data, dam_name):
    features = [
        'cloudcover', 'humidity', 'dew', 'precipcover',
        'temperature', 'windspeed', 'winddir', 'precip', 'tempmax'
    ]
    return {f"{f}-{dam_name}": day_data.get(f, 0) for f in features}

# Streamlit app starts here
st.title('Mettur Dam Storage Prediction')

# User input for date
date = st.date_input("Select Date", datetime.today())

# Fetch weather data based on user input
weather_data = fetch_weather_features(date.strftime('%Y-%m-%d'), dam_name)

if weather_data:
    # Map the fetched weather data for the selected dam
    mapped_weather_features = map_weather_features(weather_data, dam_name)

    # Display the mapped weather features
    st.write("Mapped Weather Features:", mapped_weather_features)

    # You can now proceed with your dam storage prediction logic using these features
else:
    st.write("No weather data available for this date and dam.")
