# 🏨 Hotel Booking Cancellation Prediction

A Machine Learning web application that predicts whether a hotel booking is likely to be cancelled based on customer details, booking information, reservation history and other booking-related features.

## 📌 Project Overview

Hotel booking cancellations can affect hotel revenue, room availability and business planning. This project uses Machine Learning to identify potential booking cancellations and help hotels make better business decisions.

The application provides an interactive web interface where users can enter booking details and receive cancellation predictions.

## 🚀 Features

- Predicts hotel booking cancellation.
- Interactive Streamlit dashboard.
- Machine Learning model using an Ensemble Learning approach.
- FastAPI backend for prediction requests.
- User-friendly input form.
- Real-time prediction results through the API.
- Cloud deployment support.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Model | Voting Classifier |
| Backend | FastAPI |
| Frontend | Streamlit |
| API Testing | Swagger UI |
| Model Serialization | Joblib |
| Version Control | Git & GitHub |
| Deployment | Render, Streamlit Community Cloud |

## 📊 Dataset

**Dataset:** Hotel Booking Demand Dataset

The dataset contains hotel booking information, including:

- Hotel type
- Lead time
- Arrival date
- Guest information
- Market segment
- Distribution channel
- Room type
- Deposit type
- Previous cancellations
- Customer type
- Special requests

**Target Variable:** `is_canceled`

- `0` – Booking Not Cancelled
- `1` – Booking Cancelled

## ⚙️ Model Details

**Algorithm:** Voting Classifier (Ensemble Learning)

The trained Machine Learning model is saved using Joblib and loaded by the FastAPI backend to generate predictions.

## 📂 Project Structure

```text
Hotel_Booking_Cancellation_Prediction/
│
├── fastapi_app.py
├── streamlit_app.py
├── hotel_booking_cancellation_model.joblib
├── hotel_bookings.csv
├── hotel_bookings_classification_fixed (1).py
├── requirements.txt
├── README.md
└── .gitattributes
```

## 💻 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kodevikas/Hotel_Booking_Cancellation_Prediction.git
```

### 2. Navigate to the Project Folder

```bash
cd Hotel_Booking_Cancellation_Prediction
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run FastAPI Backend

```bash
uvicorn fastapi_app:app --reload --port 8000
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### 5. Run Streamlit Frontend

Open another terminal and execute:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

## 🌐 Deployment

- **Backend:** Render
- **Frontend:** Streamlit Community Cloud

## ℹ️ About this Project

This application uses Machine Learning to predict whether a hotel booking is likely to be cancelled based on booking details, guest information, reservation history, room preferences and other characteristics.

### Model Details

**Algorithm:** Voting Classifier (Ensemble Learning)

**Backend:** FastAPI

**Frontend:** Streamlit

**Deployment:** Render + Streamlit Community Cloud

**Prediction:** Booking Cancellation / No Cancellation

*Note: This prediction is a Machine Learning estimate. Actual booking cancellations may vary depending on customer behaviour and other factors.*

---

## 👨‍💻 Author

**Vikas Kode**

GitHub: https://github.com/kodevikas

---

⭐ If you find this project useful, consider giving it a star!
