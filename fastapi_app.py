from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# 1. Load the trained Hard Voting Model

model=joblib.load("hotel_booking_cancellation_model.joblib")

# create Fastapi application

app=FastAPI(
    title="Hotel Booking Cancellation Prediction API"
    )

print("LOADED: HOTEL BOOKING CANCELLATION API")
print("MODEL:", type(model))




# 5. Input Data Validation

class HotelBooking(BaseModel):

    hotel: str
    lead_time: int
    arrival_date_year: int
    arrival_date_month: str
    arrival_date_week_number: int
    arrival_date_day_of_month: int
    stays_in_weekend_nights: int
    stays_in_week_nights: int
    adults: int
    children: float
    babies: int
    meal: str
    country: str
    market_segment: str
    distribution_channel: str
    is_repeated_guest: int
    previous_cancellations: int
    previous_bookings_not_canceled: int
    reserved_room_type: str
    assigned_room_type: str
    booking_changes: int
    deposit_type: str
    agent: str
    days_in_waiting_list: int
    customer_type: str
    adr: float
    required_car_parking_spaces: int
    total_of_special_requests: int


# 6. Home Endpoint


@app.get("/")
def home():
    return {
        "message": "Hotel Booking Cancellation Prediction API",
        "status": "API is running successfully"
    }


# 7. Prediction Endpoint


@app.post("/predict")
def predict(data: HotelBooking):

    try:

        input_data = pd.DataFrame(
            [data.model_dump()]
        )

        prediction = model.predict(input_data)

        result = int(prediction[0])

        if result == 1:
            prediction_text = "Booking will be cancelled"
        else:
            prediction_text = "Booking will not be cancelled"

        return {
            "prediction": result,
            "result": prediction_text
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



