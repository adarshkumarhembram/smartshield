# backend/routes/predict.py

from flask import Blueprint, request, jsonify, current_app
import numpy as np
import joblib
import os
from datetime import datetime

predict_route = Blueprint("predict_route", __name__)

# Load model and scaler
model_path = os.path.join("models", "fraud_model.pkl")
scaler_path = os.path.join("models", "scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

@predict_route.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json.get("features")

        if not data or len(data) != 30:
            return jsonify({"error": "Invalid input. Expecting 30 numerical features."}), 400

        # Prepare input
        input_array = np.array(data).reshape(1, -1)
        scaled_input = scaler.transform(input_array)

        # Make prediction
        prediction = model.predict(scaled_input)[0]
        probability = model.predict_proba(scaled_input)[0][1]

        result = {
            "fraud": bool(prediction),
            "confidence": round(float(probability), 4)
        }

        # Save transaction to DB
        txn_data = {
            "features": data,
            "prediction": result["fraud"],
            "confidence": result["confidence"],
            "timestamp": datetime.utcnow()
        }

        collection = current_app.config["TRANSACTIONS_COLLECTION"]
        collection.insert_one(txn_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@predict_route.route("/transactions", methods=["GET"])
def get_transactions():
    try:
        collection = current_app.config["TRANSACTIONS_COLLECTION"]
        txns = list(collection.find().sort("timestamp", -1).limit(10))

        for txn in txns:
            txn["_id"] = str(txn["_id"])
            txn["timestamp"] = txn["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(txns)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
