import streamlit as st
import google.generativeai as palm
import altair as alt


# Configure the Palm API
palm.configure(api_key="AIzaSyCDCyqSJFyuWotRLUZiZnscv29XbfaNPp8")

# Model name
model_name = "models/chat-bison-001"

# Introduction text
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

# Streamlit App Title
st.title("AI Travel Planner Itinerary")

# Inputs for number of days and destination
num_days = st.number_input("Enter the number of days for the trip:", min_value=1, max_value=30, value=3)
destination = st.text_input("Enter the destination for the trip:", "Paris")

# Button to Generate Itinerary
if st.button("Generate Itinerary"):
    # Placeholder for the generated itinerary
    itinerary = ""
    food_places = ""
    # Generate Itinerary using the selected model
    try:
        with st.spinner("Generating Itinerary..."):
            # Generate text using the model
            prompt = f"Generate an itinerary for a {num_days}-day trip to {destination}. Include details about nearby food places."
            response = palm.generate_text(model=model_name, prompt=prompt)
            itinerary = response.result  # Adjust this based on the actual response structure
    except Exception as e:
        # Display detailed error message
        st.error(f"Error generating itinerary: {e}")
        st.exception(e)
        st.warning("Please check your inputs and try again.")

    # Display the generated itinerary and food places
    if itinerary:
        st.success("Itinerary generated successfully!")
        st.text_area("Generated Itinerary:", value=itinerary, height=400)
    else:
        st.warning("No itinerary generated. Please try again with different inputs.")


