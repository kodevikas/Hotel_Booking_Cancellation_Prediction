import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Hotel Booking Prediction",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #f4f7fb;
    color: #18345b;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10264d, #173f73);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Main headings */
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #15345b !important;
}

.subtitle {
    color: #66758a !important;
    font-size: 17px;
}

.section-title {
    font-size: 23px;
    font-weight: 700;
    color: #183b67 !important;
    margin-top: 15px;
}

/* Input labels */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] span {
    color: #18345b !important;
    font-weight: 600 !important;
}

/* Input boxes */
[data-baseweb="select"] > div {
    background-color: white !important;
    border-radius: 8px;
}

[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background-color: white !important;
    color: #18345b !important;
}

/* Select box text */
[data-baseweb="select"] * {
    color: #18345b !important;
}

/* Form card */
div[data-testid="stForm"] {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e3eaf3;
}

/* Predict button */
.stButton > button,
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(90deg, #164b99, #2376c8);
    color: white !important;
    border: none;
    border-radius: 10px;
    height: 50px;
    font-weight: bold;
    font-size: 17px;
    width: 100%;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: #0d3977;
    color: white !important;
}

/* Result cards */
.result-success {
    background-color: #e8f8ef;
    border-left: 6px solid #20a464;
    padding: 20px;
    border-radius: 12px;
    color: #176b3c !important;
    font-size: 20px;
    font-weight: bold;
}

.result-danger {
    background-color: #fff0f0;
    border-left: 6px solid #e54848;
    padding: 20px;
    border-radius: 12px;
    color: #b42323 !important;
    font-size: 20px;
    font-weight: bold;
}

/* Metrics */
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e3eaf3;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("<h1>🏨</h1>", unsafe_allow_html=True)

    st.markdown("""
    # Hotel Booking
    ## Cancellation Prediction
    """)

    st.markdown("---")

    st.markdown("""
    ### Plan Smarter. Book Confidently.

    🔹 Predict booking cancellation

    🔹 Improve hotel revenue management

    🔹 Support better business decisions

    🔹 Data-driven booking analysis
    """)

    st.markdown("---")

    st.caption("Machine Learning Prediction System")


# --------------------------------------------------
# MAIN PAGE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🏨 Hotel Booking Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Predict whether a hotel booking is likely to be cancelled.</div>',
    unsafe_allow_html=True
)

st.write("")


# --------------------------------------------------
# BOOKING FORM
# --------------------------------------------------

with st.form("booking_prediction_form"):

    st.markdown(
        '<div class="section-title">📋 Booking Details</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        hotel = st.selectbox(
            "Hotel Type",
            ["Resort Hotel", "City Hotel"]
        )

        lead_time = st.number_input(
            "Lead Time (days)",
            0, 500, 100
        )

        arrival_date_year = st.selectbox(
            "Arrival Year",
            [2015, 2016, 2017]
        )

    with col2:

        arrival_date_month = st.selectbox(
            "Arrival Month",
            [
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ]
        )

        arrival_date_week_number = st.number_input(
            "Arrival Week Number",
            1, 53, 27
        )

        arrival_date_day_of_month = st.number_input(
            "Arrival Day",
            1, 31, 15
        )

    with col3:

        stays_in_weekend_nights = st.number_input(
            "Weekend Nights",
            0, 20, 1
        )

        stays_in_week_nights = st.number_input(
            "Week Nights",
            0, 50, 3
        )

        meal = st.selectbox(
            "Meal Plan",
            [
                "Bed & Breakfast (BB)",
                "Full Board (FB)",
                "Half Board (HB)",
                "Self Catering (SC)",
                "Undefined"
            ]
        )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">👥 Guest Information</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        adults = st.number_input(
            "Adults",
            0, 20, 2
        )

        children = st.number_input(
            "Children",
            0.0, 10.0, 0.0
        )

    with col2:

        babies = st.number_input(
            "Babies",
            0, 10, 0
        )

        country = st.text_input(
            "Country Code",
            "PRT"
        )

    with col3:

        is_repeated_guest = st.selectbox(
            "Repeated Guest",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        customer_type = st.selectbox(
            "Customer Type",
            ["Transient", "Transient-Party", "Contract", "Group"]
        )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🏷️ Booking & Market Information</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        market_segment = st.selectbox(
            "Market Segment",
            [
                "Online TA", "Offline TA/TO", "Direct",
                "Corporate", "Groups", "Complementary",
                "Aviation", "Undefined"
            ]
        )

        distribution_channel = st.selectbox(
            "Distribution Channel",
            ["TA/TO", "Direct", "Corporate", "GDS", "Undefined"]
        )

    with col2:

        previous_cancellations = st.number_input(
            "Previous Cancellations",
            0, 100, 0
        )

        previous_bookings_not_canceled = st.number_input(
            "Previous Bookings Not Cancelled",
            0, 100, 0
        )

    with col3:

        booking_changes = st.number_input(
            "Booking Changes",
            0, 20, 0
        )

        days_in_waiting_list = st.number_input(
            "Waiting List Days",
            0, 365, 0
        )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🛏️ Room & Payment Information</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
            

            reserved_room_type = st.selectbox(
                "Reserved Room Type",
                ["A", "B", "C", "D", "E"]
            )

            assigned_room_type = st.selectbox(
                "Assigned Room Type",
                ["A", "B", "C", "D", "E"]
            )
    with col2:

        deposit_type = st.selectbox(
            "Deposit Type",
            ["No Deposit", "Non Refund", "Refundable"]
        )

        agent = st.text_input(
            "Agent ID",
            "9"
        )

    with col3:

        adr = st.number_input(
            "ADR (Average Daily Rate)",
            0.0, 1000.0, 100.0
        )

        required_car_parking_spaces = st.number_input(
            "Parking Spaces Required",
            0, 10, 0
        )

    total_of_special_requests = st.number_input(
        "Total Special Requests",
        0, 10, 0
    )

    st.markdown("")

    predict_button = st.form_submit_button(
        "🔮 Predict Booking Status"
    )


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if predict_button:

    data = {
        "hotel": hotel,
        "lead_time": lead_time,
        "arrival_date_year": arrival_date_year,
        "arrival_date_month": arrival_date_month,
        "arrival_date_week_number": arrival_date_week_number,
        "arrival_date_day_of_month": arrival_date_day_of_month,
        "stays_in_weekend_nights": stays_in_weekend_nights,
        "stays_in_week_nights": stays_in_week_nights,
        "adults": adults,
        "children": children,
        "babies": babies,
        "meal": meal,
        "country": country,
        "market_segment": market_segment,
        "distribution_channel": distribution_channel,
        "is_repeated_guest": is_repeated_guest,
        "previous_cancellations": previous_cancellations,
        "previous_bookings_not_canceled": previous_bookings_not_canceled,
        "reserved_room_type": reserved_room_type,
        "assigned_room_type": assigned_room_type,
        "booking_changes": booking_changes,
        "deposit_type": deposit_type,
        "agent": agent,
        "days_in_waiting_list": days_in_waiting_list,
        "customer_type": customer_type,
        "adr": adr,
        "required_car_parking_spaces": required_car_parking_spaces,
        "total_of_special_requests": total_of_special_requests
    }

    # API REQUEST
    with st.spinner("Analyzing booking details..."):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=data,
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                prediction = result["prediction"]
                message = result["result"]

                st.markdown("---")

            

                # --------------------------------------------------
                # PREDICTION RESULT
                # --------------------------------------------------

                st.markdown("---")

                st.markdown(
                    "<h2 style='color: #18345B;'>📊 Prediction Result</h2>",
                    unsafe_allow_html=True
                )

                if prediction == 1:

                    st.markdown(
                        """
                        <div style="
                            background-color: #FFF5F5;
                            border-left: 4px solid #DC2626;
                            padding: 15px 20px;
                            border-radius: 8px;
                            margin-top: 10px;
                        ">
                            <h3 style="color: #B91C1C; margin: 0;">
                                ⚠️ Booking is likely to be cancelled
                            </h3>
                            <p style="color: #7F1D1D; margin-top: 8px;">
                                This booking has a higher predicted cancellation risk.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        """
                        <div style="
                            background-color: #F0FDF4;
                            border-left: 4px solid #16A34A;
                            padding: 15px 20px;
                            border-radius: 8px;
                            margin-top: 10px;
                        ">
                            <h3 style="color: #15803D; margin: 0;">
                                ✅ Booking will not be cancelled
                            </h3>
                            <p style="color: #166534; margin-top: 8px;">
                                This booking is predicted to be retained.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:

                st.error(
                    f"Prediction failed: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI server is not running. "
                "Please start the backend first."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request timed out. Please try again."
            )

        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )

    
# About This Project
st.markdown("---")

st.markdown("""
<div style="
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #E3EAF3;
    margin-top: 20px;
">

<h3 style="color: #18345B;">ℹ️ About this Project</h3>

<p style="color: #52647A; font-size: 16px;">
This application uses Machine Learning to predict whether a hotel booking
is likely to be cancelled based on booking details, guest information,
reservation history, room preferences and other characteristics.
</p>

<h3 style="color: #18345B;">⚙️ Model Details</h3>

<p style="color: #52647A; font-size: 15px; line-height: 1.9;">
<b>Algorithm:</b> Voting Classifier (Ensemble Learning)<br>
<b>Backend:</b> FastAPI<br>
<b>Frontend:</b> Streamlit<br>
<b>Deployment:</b> Vercel
</p>

<p style="color: #7A8798; font-size: 13px;">
<i>Note: This prediction is a Machine Learning estimate.
Actual booking cancellations may vary depending on customer behaviour
and other factors.</i>
</p>

</div>
""", unsafe_allow_html=True)
