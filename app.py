import streamlit as st
from datetime import datetime, timedelta, time

# Title and Version
st.title("Dripdok Jetlag Calculator")
st.caption("V2.0b 2024")

# Input fields for Origin Departure Date and Time
origin_date = st.date_input("Origin Departure Date")
origin_time = st.time_input("Origin Departure Time (AM/PM)", time(12, 0))  # Default to 12:00 PM
origin_departure_time = datetime.combine(origin_date, origin_time)

# Input fields for Destination Arrival Date and Time
destination_date = st.date_input("Destination Arrival Date")
destination_time = st.time_input("Destination Arrival Time (AM/PM)", time(12, 0))  # Default to 12:00 PM
destination_arrival_time = datetime.combine(destination_date, destination_time)

# Input for Year of Birth
dob_year = st.number_input("Year of Birth", min_value=1900, max_value=datetime.now().year, value=1990)

# Input for Grogginess Level
grogginess_level = st.selectbox("Grogginess Level", ["Low", "Moderate", "High"])

# Option for Oral NMN usage
oral_nmn = st.selectbox("Will you use Oral NMN?", ["yes", "no"])

# Optional input for Return Flight Information
return_flight = st.selectbox("Do you have return flight information?", ["no", "yes"])

if return_flight == "yes":
    return_departure_date = st.date_input("Return Flight Departure Date")
    return_departure_time = st.time_input("Return Flight Departure Time (AM/PM)", time(12, 0))  # Default to 12:00 PM
    return_departure_time = datetime.combine(return_departure_date, return_departure_time)

    return_date = st.date_input("Return Flight Arrival Date")
    return_time = st.time_input("Return Flight Arrival Time (AM/PM)", time(12, 0))  # Default to 12:00 PM
    return_arrival_time = datetime.combine(return_date, return_time)
else:
    return_arrival_time = None
    return_departure_time = None

# Calculate Dosage and Drip Duration
if st.button("Calculate"):
    # Age-based and grogginess-based NMN oral dosage
    current_year = datetime.now().year
    age = current_year - dob_year

    # Dynamic NMN Dosage based on grogginess and age
    if oral_nmn == "yes":
        if age > 50 or grogginess_level == "High":
            oral_nmn_dosage = 1000
        elif 30 < age <= 50 or grogginess_level == "Moderate":
            oral_nmn_dosage = 750
        else:
            oral_nmn_dosage = 500

    # NAD IV Dosage and Drip Duration based on Age
    if age >= 40:
        recommended_nad_dose = 500
        iv_duration = 90 if age > 60 else 60  # Longer duration for older age to reduce tolerance issues
    else:
        recommended_nad_dose = 250
        iv_duration = 45

    # Schedule for IV treatment before and after flight
    pre_flight_iv_time = origin_departure_time - timedelta(hours=24)
    post_arrival_iv_time = destination_arrival_time + timedelta(hours=24)

    # Optional: Post-return IV treatment schedule
    if return_flight == "yes":
        post_return_iv_time = return_arrival_time + timedelta(hours=24)
    else:
        post_return_iv_time = None

    # Oral NMN schedule for the week following arrival
    oral_nmn_schedule = []
    if oral_nmn == "yes":
        current_day = destination_arrival_time
        for day in range(7):  # Schedule for 1 week
            oral_nmn_schedule.append({
                "date": (current_day + timedelta(days=day)).strftime("%Y-%m-%d"),
                "best_time": "09:00 AM",  # Suggested time for NMN
                "dosage": f"{oral_nmn_dosage} mg"
            })

    # Display the calculated results
    st.subheader("Recommendations")

    st.markdown("**Pre-Flight IV Treatment**")
    st.write(f"Dosage: {recommended_nad_dose} mg NAD")
    st.write(f"Time: {pre_flight_iv_time.strftime('%Y-%m-%d %I:%M %p')}")
    st.write(f"Drip Duration: {iv_duration} minutes")

    st.markdown("**Post-Arrival IV Treatment**")
    st.write(f"Dosage: {recommended_nad_dose} mg NAD")
    st.write(f"Time: {post_arrival_iv_time.strftime('%Y-%m-%d %I:%M %p')}")
    st.write(f"Drip Duration: {iv_duration} minutes")

    if return_flight == "yes":
        st.markdown("**Post-Return IV Treatment**")
        st.write(f"Dosage: {recommended_nad_dose} mg NAD")
        st.write(f"Time: {post_return_iv_time.strftime('%Y-%m-%d %I:%M %p')}")
        st.write(f"Drip Duration: {iv_duration} minutes")

    if oral_nmn_schedule:
        st.markdown("**Oral NMN Schedule (Post-Arrival)**")
        for day in oral_nmn_schedule:
            st.write(f"{day['date']} at {day['best_time']} - Dosage: {day['dosage']}")

    # Add link to Dripdok at the bottom
    st.markdown(
        "[Visit Dripdok To Get Your NMN or NAD IV Today!](https://wa.me/6281804608182)", 
        unsafe_allow_html=True
    )