# Importing the libraries
import streamlit as st
import numpy as np
import pickle
from datetime import datetime

# Loading the model
with open("models/flight_price_predictor_cv.pkl", mode='rb') as file:
    predictor = pickle.load(file)

# Setting up the frontend app

# Heading and Title
st.title("Flight Price Predictor App")
st.write("Enter flight detials to predict the price:")

# Setting up the Input fields
airline = st.selectbox("AIRLINE", ['Jet Airways', 'Indigo', 'Air India', 'Multple carriers', 
                                   'Spicejet', 'Vistara', 'Air Asia', 'GoAir',
                                   'Multiple carriers Premium economy', 'Jet Airways Business',
                                   'Vistara Premium economy', 'Trujet'])

source = st.selectbox("SOURCE", ['Delhi', 'Kolkata', 'Bangalore', 'Mumbai', 'Chennai'])
destination = st.selectbox("DESTINATION", ['Cochin', 'Bangalore', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])

total_stops = st.selectbox("STOPS", ['non-stop', '1 stop', '2 stops', '3 stops', '4 stops'])

journey_date = st.date_input("Journey Date", min_value=datetime.today())
departure_time = st.time_input("Departure Time")
arrival_time = st.time_input("Arrival Time")

# Preprocessing and setting up the data
def preprocess():
    try:
        # Date breakdown
        journey_day = journey_date.day
        journey_month = journey_date.month

        # Departure and Arrival Time breakdown
        departure_hour = departure_time.hour
        departure_minute = departure_time.minute
        arrival_hour = arrival_time.hour
        arrival_minute = arrival_time.minute

        # Duration calculation
        departure_date = datetime.strptime(f"{journey_date} {departure_time}", "%Y-%m-%d %H:%M:%S")
        arrival_date = datetime.strptime(f"{journey_date} {arrival_time}", "%Y-%m-%d %H:%M:%S")
        duration = (arrival_date - departure_date).total_seconds() / 60
        duration_hour = int(duration // 60)
        duration_minute = int(duration % 60)

        # Mapping total stops
        stop_map = {'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4}
        stops = stop_map[total_stops]

        # Encoding the Airline, Source and Destination
        if airline == 'Air Asia':
            airline_encoded = [0 for x in ['Air India', 'GoAir', 'Indigo', 'Jet Airways', 
                                           'Jet Airways Business', 'Multple carriers',
                                           'Multiple carriers Premium economy', 'Spicejet', 'Trujet',
                                           'Vistara', 'Vistara Premium economy']]
        else:
            airline_encoded = [1 if airline == x else 0 for x in
                            ['Air India', 'GoAir', 'Indigo', 'Jet Airways', 
                            'Jet Airways Business', 'Multple carriers',
                            'Multiple carriers Premium economy', 'Spicejet', 'Trujet',
                            'Vistara', 'Vistara Premium economy']]
        
        if source == 'Bangalore':
            source_encoded = [0 for x in ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']]
        else:
            source_encoded = [1 if source == x else 0 for x in ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']]
        
        if destination == 'Bangalore':
            destination_encoded = [0 for x in ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi']]
        else:
            destination_encoded = [1 if destination == x else 0 for x in
                                ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi']]
        
        # Final Input Vector (length = 29)
        final_input = airline_encoded + source_encoded + destination_encoded + [stops, journey_day, 
                                                                                journey_month, departure_hour,
                                                                                departure_minute, arrival_hour,
                                                                                arrival_minute, duration_hour, duration_minute]
        
        # Converting input vetor into an array and reshaping it
        final_input_reshaped = np.array(final_input).reshape(1, -1)

        # Returning the final input vector
        return final_input_reshaped
    
    except Exception as e:
        st.error(f"[Info] Error duirng preprocessing: {e}")
        return None
    
# Prediction and Predict button
if st.button('Predict PRICE'):
    # Preprocessing the data for the model
    preprocessed_data = preprocess()

    if preprocessed_data is not None:
        try:
            predicted_price = predictor.predict(preprocessed_data)[0]
            st.success(f"The estimated ticket price: ₹{round(predicted_price, 2)}")
        except Exception as e:
            st.error(f"[Info] Error during prediction: {e}")