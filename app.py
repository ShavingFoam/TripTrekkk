import streamlit as st
import google.generativeai as palm
import requests
import datetime

# Configure the API key for Google Generative AI
palm.configure(api_key="AIzaSyC_35phqz4upg8YNhImHjeonSRzg6xI5b4")

# Use the text-bison-001 model
model_name = "models/text-bison-001"

# Amadeus API credentials
api_key = 'ut8iytfAocjtG0qvhaxSpQ6mMdOLho1O'
api_secret = '0IrufdJU2J4DjExp'

def get_amadeus_access_token(api_key, api_secret):
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data["access_token"]

def get_flight_details(access_token, origin, destination, departure_date):
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={destination}&departureDate={departure_date}&adults=1&max=5"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        st.error(f"Error fetching flight details: {response.status_code} {response.reason}")
        return None

def convert_currency(amount, from_currency="EUR", to_currency="INR"):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        rates = response.json()["rates"]
        return amount * rates[to_currency]
    else:
        st.error("Error fetching exchange rates.")
        return amount

st.markdown("""
# TripTrek: Intelligent Travel Planning with AI
TripTrek is an AI-powered travel planning platform designed to revolutionize the way people plan and organize their trips. By leveraging advanced AI.

## Scenario 1: Family Vacation Coordination
TripTrek helps families plan their vacations by taking user inputs such as destination and number of days to generate a detailed itinerary. It suggests suitable activities, restaurants, and accommodations tailored to family needs.

## Scenario 2: Business Travel Planning for Professionals
TripTrek streamlines business travel for professionals by taking user inputs like destination and number of days to create a comprehensive itinerary that includes meetings, conferences, and networking events.

## Scenario 3: Educational Trip for Students
TripTrek assists in planning educational trips for students by taking inputs like destination and number of days to produce a structured itinerary with educational activities, museum visits, and learning opportunities.
""")

st.title("AI Travel Planner Itinerary")

num_days = st.number_input("Enter the number of days for the trip:", min_value=1, max_value=30, value=3)
destination = st.text_input("Enter the destination for the trip (IATA code):", "SIN")
origin = st.text_input("Enter your origin city (IATA code):", "CJB")
departure_date = st.date_input("Enter your departure date:", datetime.date.today())
hotel_type = st.selectbox(
    "Select the type of hotel you are looking forward to stay:",
    ("Budget", "Comfort", "Luxury")
)

if st.button("Generate Itinerary"):
    itinerary = ""
    flight_details = ""
    try:
        with st.spinner("Generating Itinerary..."):
            # Generate text using the model
            prompt = (f"Generate an itinerary for a {num_days}-day trip to {destination}. "
                      f"Include details about nearby food places and the best {hotel_type.lower()} hotels/hostels in the city.")
            response = palm.generate_text(model=model_name, prompt=prompt)
            itinerary = response.result  # Adjust this based on the actual response structure

        # Fetch flight details using Amadeus API
        access_token = get_amadeus_access_token(api_key, api_secret)
        flight_response = get_flight_details(access_token, origin.upper(), destination.upper(), departure_date)
        
        if flight_response:
            for flight in flight_response:
                airline = flight['itineraries'][0]['segments'][0]['carrierCode']
                price_eur = float(flight['price']['total'])
                price_inr = convert_currency(price_eur, "EUR", "INR")
                departure = flight['itineraries'][0]['segments'][0]['departure']['at']
                arrival = flight['itineraries'][0]['segments'][0]['arrival']['at']
                flight_details += f"Airline: {airline}, Price: {price_inr:.2f} INR, Departure: {departure}, Arrival: {arrival}\n"
    except Exception as e:
        st.error(f"Error generating itinerary or fetching flight details: {e}")

    # Display the generated itinerary and flight details
    if itinerary:
        st.success("Itinerary generated successfully!")
        st.text_area("Generated Itinerary:", value=itinerary, height=300)
        st.text_area("Flight Details:", value=flight_details, height=200)
    else:
        st.warning("No itinerary generated. Please try again with different inputs.")
