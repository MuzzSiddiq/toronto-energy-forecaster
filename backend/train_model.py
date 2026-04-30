import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib # Used to save the model for the API later
import os

# 1. Load the merged data
df = pd.read_csv("../data/processed/toronto_energy_final.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 2. The Temporal Split (Train on 2023-2024, Test on 2025)
# This is a "backtest" to see how we would have performed in 2025
train = df[df['timestamp'].dt.year < 2025]
test = df[df['timestamp'].dt.year == 2025]

# 3. Select Features (X) and Target (y)
features = ['Temp (°C)', 'Rel Hum (%)', 'Wind Spd (km/h)', 'hour', 'day_of_week', 'is_weekend']
target = 'Toronto'

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

# 4. Initialize and Train the Model
print("Training the Council of Trees (Random Forest)...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Make Predictions on the "Future" (2025)
predictions = model.predict(X_test)

# 6. Evaluate: How good are we?
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
avg_demand = y_test.mean()
accuracy_pct = 100 - (mae / avg_demand * 100)

print(f"--- Results ---")
print(f"Mean Absolute Error (MAE): {mae:.2f} MW")
print(f"Average Demand: {avg_demand:.2f} MW")
print(f"Estimated Accuracy: {accuracy_pct:.2f}%")

# 7. Save the model to a file so the API can use it later
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/toronto_energy_model.pkl")
print("Model saved to backend/models/toronto_energy_model.pkl")

# Check Feature Importance
importances = model.feature_importances_
feature_names = features
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
print("\n--- Feature Importance ---")
print(feature_importance_df.sort_values(by='Importance', ascending=False))