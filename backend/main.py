from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from sqlalchemy import create_engine, text
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Toronto Pluse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd specify the React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Load the ML Model at startup
MODEL_PATH = "backend/models/toronto_energy_model.pkl" # edited this line to reflect actual path - make sure its right
model = joblib.load(MODEL_PATH)

# 2. Database Connection
DATABASE_URL = "postgresql://user:password@localhost:5432/toronto_pulse"
engine = create_engine(DATABASE_URL)


# 3. Define the "Shape" of data the API expects (Pydantic)
class PredictionInput(BaseModel):
    temp: float
    humidity: float
    wind_speed: float
    hour: int
    day_of_week: int
    is_weekend: int


@app.get("/")
def home():
    return {"status": "Toronto Pulse API is live"}


@app.get("/history")
def get_history(limit: int = 24):
    """Fetches the last X hours of actual demand from SQL"""
    # query = text("SELECT timestamp, demand_mw FROM energy_data ORDER BY timestamp DESC LIMIT :limit")
    query = text('SELECT "timestamp", "Toronto" FROM energy_data ORDER BY "timestamp" DESC LIMIT :limit')
    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})
        data = [{"timestamp": row[0], "demand": row[1]} for row in result]
    return data


@app.post("/predict")
def predict_energy(data: PredictionInput):
    """Uses the Random Forest model to predict demand based on input"""
    # Convert input to the format the model expects
    input_df = pd.DataFrame([data.dict().values()],
                            columns=['Temp (°C)', 'Rel Hum (%)', 'Wind Spd (km/h)', 'hour', 'day_of_week',
                                     'is_weekend'])

    prediction = model.predict(input_df)[0]
    return {"predicted_demand_mw": round(prediction, 2)}