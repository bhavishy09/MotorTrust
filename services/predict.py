import os
import pickle
import numpy as np
from datetime import datetime
import re

MODEL_PATH = 'models/car_price_model.pkl'

def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                return pickle.load(f)
        else:
            print(f"Model file not found at {MODEL_PATH}")
            return None
    except Exception as e:
        print(f"Error loading model from {MODEL_PATH}: {e}")
        return None

model = load_model()

def get_car_price_prediction(year, present_price, km_driven, fuel_type, seller_type, transmission):
    if model is None:
        # Fallback if model is not loaded
        return present_price * 0.65
    
    fuel_encoded = 1 if fuel_type == 'Petrol' else 0
    seller_encoded = 1 if seller_type == 'Individual' else 0
    transmission_encoded = 1 if transmission == 'Manual' else 0
    current_year = datetime.now().year
    years_old = current_year - year

    features = np.array([[present_price, km_driven, fuel_encoded, 
                          seller_encoded, transmission_encoded, years_old]])
    
    predicted_price = float(model.predict(features)[0])
    return predicted_price
