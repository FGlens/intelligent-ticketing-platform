import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

print("Loading dataset...")

# Load the public dataset
df = pd.read_csv('data/cinema_hall_ticket_sales.csv')

print("Dataset loaded successfully!")
print("Total records:", len(df))
print("Columns:", df.columns.tolist())
print()

# Clean the Number_of_Person column (some values are "Alone")
df['Number_of_Person'] = df['Number_of_Person'].replace('Alone', 1)
df['Number_of_Person'] = pd.to_numeric(df['Number_of_Person'], errors='coerce')
df = df.dropna(subset=['Number_of_Person'])

# Encode categorical columns
le_genre = LabelEncoder()
le_seat = LabelEncoder()

df['Movie_Genre_encoded'] = le_genre.fit_transform(df['Movie_Genre'])
df['Seat_Type_encoded'] = le_seat.fit_transform(df['Seat_Type'])

# Features and Target
# We predict Number_of_Person as a proxy for ticket demand
X = df[['Age', 'Ticket_Price', 'Movie_Genre_encoded', 'Seat_Type_encoded']]
y = df['Number_of_Person']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluation Metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("=" * 55)
print("LINEAR REGRESSION MODEL EVALUATION (Public Dataset)")
print("=" * 55)
print(f"Mean Absolute Error (MAE):     {mae:.4f}")
print(f"Root Mean Square Error (RMSE): {rmse:.4f}")
print(f"R² Score:                      {r2:.4f}")
print("=" * 55)

# Save the model
os.makedirs('data/models', exist_ok=True)
joblib.dump(model, 'data/models/demand_model.joblib')
print("\nModel saved successfully to data/models/demand_model.joblib")