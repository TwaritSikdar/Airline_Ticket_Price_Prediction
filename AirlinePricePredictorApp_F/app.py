from flask import Flask, render_template, request
import joblib
from datetime import datetime, timedelta
import numpy as np

# Loading the model
try:
    predictor = joblib.load("models/flight_price_predictor_cv.pkl")
except FileNotFoundError:
    predictor = None

# App Iniitialization
predictor_app = Flask(__name__)

# Defining function for the app
@predictor_app.route("/", methods=["GET", "POST"])
def predict():
    prediction_text = ''

    # Preprocessing the form data
    if request.method == 'POST':
        try:
            # Retrieving data from the request
            airline = str(request.form.get("Airline"))
            source = str(request.form.get("Source"))
            destination = str(request.form.get("Destination"))
            total_stops = str(request.form.get("Total_Stops"))
            journey_date = datetime.strptime(request.form.get("Journey_date"), "%Y-%m-%d")
            departure_time = datetime.strptime(request.form.get("Departure_time"), "%H:%M").time()
            arrival_time = datetime.strptime(request.form.get("Arrival_time"), "%H:%M").time()

            # Encoding airline, source, destination and total_stops(mapping)

            # airline 
            airlines = ['Air India', 'GoAir', 'Indigo', 'Jet Airways', 'Jet Airways Business', 'Multple carriers', 
                        'Multiple carriers Premium economy', 'Spicejet', 'Trujet', 'Vistara', 'Vistara Premium economy']
            if airline == 'Air Asia':
                airline_encoded = [0 for x in airlines]
            else:
                airline_encoded = [1 if airline == x else 0 for x in airlines]

            # source
            sources = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
            if source == 'Bangalore':
                source_encoded = [0 for x in sources]
            else:
                source_encoded = [1 if source == s else 0 for s in sources]

            # destination
            destinations = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi']
            if destination == 'Bangalore':
                destination_encoded = [0 for x in destinations]
            else:
                destination_encoded = [1 if destination == d else 0 for d in destinations]

            # total_stops(mapping)
            stops_map = {'non-stop': 0, '1 Stop': 1, '2 Stops': 2, '3 Stops': 3, '4 Stops': 4}
            stops = stops_map[total_stops]

            # Breaking down journey_date, departure_time and arrival_time

            # journey_date into month and date
            journey_day = journey_date.day
            journey_month = journey_date.month

            # departure_time and arrival_time into hours and minutes
            departure_hours = departure_time.hour
            departure_minutes = departure_time.minute
            arrival_hours = arrival_time.hour
            arrival_minutes = arrival_time.minute

            # Duration calculation
            departure_datetime = datetime.combine(journey_date, departure_time)
            arrival_datetime = datetime.combine(journey_date, arrival_time)

            if arrival_datetime < departure_datetime:
                arrival_datetime += timedelta(days=1)

            duration = (arrival_datetime - departure_datetime).total_seconds() / 60
            duration_hours = int(duration // 60)
            duration_minutes = int(duration % 60)

            # Creating a final input vector (length=29)
            final_input_vector = airline_encoded + source_encoded + destination_encoded + [stops, journey_day,
                                journey_month, departure_hours, departure_minutes, arrival_hours,
                                arrival_minutes, duration_hours, duration_minutes]
            
            # Reshaping the input vector
            final_input_reshaped = np.array(final_input_vector).reshape(1, -1)

            # Making a prediction
            if predictor:
                predicted_price = predictor.predict(final_input_reshaped)[0]
                prediction_text = f'The estimated price is ₹{predicted_price:,.2f}. Accuracy: 93.86%'
            else:
                prediction_text = "Model file not found. Please check the path."
        except Exception as e:
            prediction_text = f"[Info] Error during prediction: {e}"
   
    # Rendering the frontend code with prediction
    return render_template("index.html", prediction=prediction_text)

# Running the App
if __name__ == "__main__":
    predictor_app.run()