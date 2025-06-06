import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load(r'D:\Amazon Delivery Project\Scripts\best_model.pkl')

# Encoders (based on training, use same order)
weather_map = {'Sunny': 4, 'Stormy': 3, 'Windy': 2, 'Cloudy': 1, 'Fog': 0}
traffic_map = {'Low': 2, 'Medium': 1, 'Jam': 0}
vehicle_map = {'Bike': 0, 'Car': 1, 'Scooter': 2}
area_map = {'Urban': 1, 'Metropolitan': 0}
category_map = {'Food': 2, 'Grocery': 1, 'Clothing': 0}
day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
    'Friday': 4, 'Saturday': 5, 'Sunday': 6}

# UI
st.title("🕐 Amazon Delivery Time Predictor")

st.write("Enter delivery details to predict estimated time (in hours).")

# User Inputs
distance = st.slider("Distance (in km)", 0.5, 50.0, 5.0)
agent_age = st.slider("Agent Age", 18, 60, 30)
agent_rating = st.slider("Agent Rating", 0.0, 5.0, 4.5, step=0.1)
weather = st.selectbox("Weather", list(weather_map.keys()))
traffic = st.selectbox("Traffic", list(traffic_map.keys()))
vehicle = st.selectbox("Vehicle", list(vehicle_map.keys()))
area = st.selectbox("Area Type", list(area_map.keys()))
category = st.selectbox("Product Category", list(category_map.keys()))
order_hour = st.slider("Order Hour (0-23)", 0, 23, 14)
day_of_week = st.selectbox("Day of Week", list(day_map.keys()))

# Prepare input
input_df = pd.DataFrame([[
    agent_age,
    agent_rating,
    weather_map[weather],
    traffic_map[traffic],
    vehicle_map[vehicle],
    area_map[area],
    category_map[category],
    distance,
    order_hour,
    day_map[day_of_week]
]], columns=[
    'Agent_Age', 'Agent_Rating', 'Weather', 'Traffic', 'Vehicle', 'Area',
    'Category', 'Distance_km', 'Order_Hour', 'Order_DayOfWeek'
])

# Prediction
if st.button("Predict Delivery Time"):
    pred = model.predict(input_df)[0]
    st.success(f"📦 Estimated Delivery Time: {pred:.2f} hours")