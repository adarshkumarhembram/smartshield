# backend/app.py

from flask import Flask
from flask_cors import CORS
from routes.predict import predict_route
from dotenv import load_dotenv
from pymongo import MongoClient
import os

# Load .env variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["smartshield"]
transactions = db["transactions"]

# Share collection with routes
app.config["TRANSACTIONS_COLLECTION"] = transactions

# Register route
app.register_blueprint(predict_route)

@app.route("/")
def home():
    return {"message": "SmartShield Backend Running ✅"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
