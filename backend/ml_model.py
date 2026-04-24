import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("dataset/sensor_data.csv")

# Create labels (IMPORTANT FIX)
def get_status(row):
    if row['mq135'] < 300:
        return "Good"
    elif row['mq135'] < 500:
        return "Fair"
    elif row['mq135'] < 800:
        return "Bad"
    else:
        return "Hazard"

data['status'] = data.apply(get_status, axis=1)

# Features & label
X = data[['mq7', 'mq135', 'temperature', 'humidity']]
y = data['status']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

joblib.dump(model, "air_quality_model.pkl")

print(" Model trained successfully")