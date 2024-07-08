import streamlit as st
import google.generativeai as palm
import altair as alt

palm.configure(api_key="AIzaSyA80czwNit7MrtUQRG5LBSla6mRQHN27j0")

model_name = "models/text-bison-001"

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
destination = st.text_input("Enter the destination for the trip:", "Paris")

if st.button("Generate Itinerary"):
    itinerary = ""
    food_places = ""
    try:
        with st.spinner("Generating Itinerary..."):
            prompt = f"Generate an itinerary for a {num_days}-day trip to {destination}. Include details about nearby food places."
            response = palm.generate_text(model=model_name, prompt=prompt)
            itinerary = response.result 
    except Exception as e:
        st.error(f"Error generating itinerary: {e}")
        st.exception(e)
        st.warning("Please check your inputs and try again.")

    if itinerary:
        st.success("Itinerary generated successfully!")
        st.text_area("Generated Itinerary:", value=itinerary, height=400)
    else:
        st.warning("No itinerary generated. Please try again with different inputs.")
    else:
        st.warning("No itinerary generated. Please try again with different inputs.")


