import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

print("Creating a placeholder ML model for car price prediction...")

X_sample = np.array([
    [8.5, 45000, 1, 0, 1, 6],
    [5.2, 72000, 0, 1, 1, 8],
    [12.0, 15000, 1, 0, 0, 2],
    [7.8, 35000, 1, 1, 1, 5],
])

y_sample = np.array([5.5, 2.8, 9.5, 5.2])

model = LinearRegression()
model.fit(X_sample, y_sample)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✓ Placeholder model created successfully: model.pkl")
print("\nNote: This is a simple demonstration model.")
print("For production use, train a proper model with real car pricing data.")
