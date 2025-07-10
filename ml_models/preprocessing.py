# preprocessing.py

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import os

def preprocess_and_save():
    print("🔄 Loading dataset...")
    df = pd.read_csv('../dataset/creditcard.csv')

    # Drop target
    X = df.drop(['Class'], axis=1)
    y = df['Class']

    print("📊 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)

    print("⚖️ Applying SMOTE to handle imbalance...")
    smote = SMOTE(random_state=42)
    X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

    print("📏 Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_bal)
    X_test_scaled = scaler.transform(X_test)

    # Save preprocessed data (optional)
    print("💾 Saving preprocessed data...")
    np.save('X_train_scaled.npy', X_train_scaled)
    np.save('X_test_scaled.npy', X_test_scaled)
    np.save('y_train_bal.npy', y_train_bal)
    np.save('y_test.npy', y_test)

    # Save scaler for backend use
    joblib.dump(scaler, '../backend/models/scaler.pkl')

    print("✅ Preprocessing complete and files saved.")

if __name__ == "__main__":
    os.makedirs("../backend/models", exist_ok=True)
    preprocess_and_save()
