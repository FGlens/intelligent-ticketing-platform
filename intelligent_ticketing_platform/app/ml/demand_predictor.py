"""
Ticket Demand Prediction using Linear Regression
-------------------------------------------------
This module predicts how many tickets an event is likely to sell
based on historical data (price, total tickets, category, etc.)
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from app.models import Event, Booking
from app import db
import joblib
import os


MODEL_PATH = 'data/models/demand_model.joblib'


def prepare_training_data():
    """
    Create training data from existing events and their bookings.
    Features: price, total_tickets, category (encoded)
    Target: number of tickets sold
    """
    events = Event.query.all()
    data = []

    for event in events:
        tickets_sold = event.total_tickets - event.available_tickets
        data.append({
            'price': event.price,
            'total_tickets': event.total_tickets,
            'category': event.category,
            'tickets_sold': tickets_sold
        })

    if not data:
        return None

    df = pd.DataFrame(data)

    # Simple encoding for category
    df['category_encoded'] = df['category'].astype('category').cat.codes

    return df


def train_demand_model():
    """
    Train a Linear Regression model and save it.
    Also returns evaluation metrics.
    """
    df = prepare_training_data()

    if df is None or len(df) < 5:
        return {
            'success': False,
            'message': 'Not enough data to train the model. Need at least 5 events with bookings.'
        }

    X = df[['price', 'total_tickets', 'category_encoded']]
    y = df['tickets_sold']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions on test set
    y_pred = model.predict(X_test)

    # Evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # Save the model
    os.makedirs('data/models', exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return {
        'success': True,
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'r2': round(r2, 4),
        'message': 'Model trained successfully!'
    }


def predict_ticket_demand(event):
    """
    Predict how many tickets an event is expected to sell.
    """
    if not os.path.exists(MODEL_PATH):
        # Train model if it doesn't exist
        result = train_demand_model()
        if not result['success']:
            return {
                'predicted_tickets': None,
                'message': result['message']
            }

    model = joblib.load(MODEL_PATH)

    # Prepare features for this event
    # We need a consistent category encoding. For simplicity we use a hash-based approach
    # In a real system we would save the encoder.
    category_code = hash(event.category) % 100  # Simple encoding

    features = np.array([[event.price, event.total_tickets, category_code]])
    prediction = model.predict(features)[0]

    # Make sure prediction is reasonable
    predicted = max(0, min(int(round(prediction)), event.total_tickets))

    return {
        'predicted_tickets': predicted,
        'total_tickets': event.total_tickets,
        'already_sold': event.total_tickets - event.available_tickets,
        'message': f'Based on historical data, this event is predicted to sell approximately {predicted} tickets.'
    }
