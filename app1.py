import streamlit as st
import pandas as pd
import joblib
from geopy.distance import geodesic
import datetime

st.title("📦 Amazon Delivery Time Predictor")

st.markdown("### 📊 Visual Insights")

# Move model loading inside the prediction button
@st.cache_resource
def load_model():
    return joblib.load('delivery_model.pkl')

st.markdown("Enter order details below to predict delivery time:")

# Inputs
agent_age = st.slider("Agent Age", 18, 60, 30)
agent_rating = st.slider("Agent Rating", 1.0, 5.0, 4.5)
store_lat = st.number_input("Store Latitude", value=12.9716)
store_lon = st.number_input("Store Longitude", value=77.5946)
drop_lat = st.number_input("Drop Latitude", value=12.9352)
drop_lon = st.number_input("Drop Longitude", value=77.6141)
order_time = st.time_input("Order Time", datetime.time(12, 0))
order_date = st.date_input("Order Date", datetime.date.today())
weather_options = ['Sunny', 'Rainy', 'Fog', 'Stormy', 'Windy']
traffic_options = ['Low', 'Medium', 'High', 'Jam']

weather = st.selectbox("Weather Condition", weather_options)
traffic = st.selectbox("Traffic Condition", traffic_options)

weather_map = {'Sunny': 0, 'Rainy': 1, 'Fog': 2, 'Stormy': 3, 'Windy': 4}
traffic_map = {'Low': 0, 'Medium': 1, 'High': 2, 'Jam': 3}

weather_encoded = weather_map[weather]
traffic_encoded = traffic_map[traffic]

if st.button("Predict Delivery Time"):
    model = load_model()  # Load model only when needed

    distance = geodesic((store_lat, store_lon), (drop_lat, drop_lon)).km
    order_hour = order_time.hour
    order_day = order_date.weekday()

    input_data = pd.DataFrame([[agent_age, agent_rating, distance, order_hour, order_day, weather_encoded, traffic_encoded]],
                              columns=['Agent_Age', 'Agent_Rating', 'Distance_km', 'Order_Hour', 'Order_Day', 'Weather', 'Traffic'])

    prediction = model.predict(input_data)[0]
    st.success(f"🚚 Estimated Delivery Time: {prediction:.2f} hours")