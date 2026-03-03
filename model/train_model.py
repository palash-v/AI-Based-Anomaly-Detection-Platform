import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Load dataset
data = pd.read_csv("data/live_vitals.csv")

# Remove timestamp
data = data.drop(columns=["timestamp"])

print("Dataset shape:", data.shape)

# -----------------------------
# Feature Scaling (VERY IMPORTANT)
# -----------------------------
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Train Isolation Forest
model = IsolationForest(
    n_estimators=200,
    contamination=0.12,   # around 10–15% abnormal expected
    random_state=42
)

model.fit(scaled_data)

# Save model AND scaler
joblib.dump(model, "model/anomaly_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("Model and scaler saved successfully!")