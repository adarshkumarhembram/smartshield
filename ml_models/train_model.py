# train_model.py

import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

def load_data():
    X_train = np.load('X_train_scaled.npy')
    X_test = np.load('X_test_scaled.npy')
    y_train = np.load('y_train_bal.npy')
    y_test = np.load('y_test.npy')
    return X_train, X_test, y_train, y_test

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print("📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f"🎯 ROC AUC Score: {auc:.4f}")
    return auc

def train_and_select_best_model():
    X_train, X_test, y_train, y_test = load_data()

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=100),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    }

    best_model = None
    best_auc = 0
    best_name = ""

    for name, model in models.items():
        print(f"\n🔁 Training {name}...")
        model.fit(X_train, y_train)
        auc = evaluate_model(model, X_test, y_test)

        if auc > best_auc:
            best_auc = auc
            best_model = model
            best_name = name

    # Save best model
    print(f"\n✅ Best Model: {best_name} with AUC: {best_auc:.4f}")
    joblib.dump(best_model, '../backend/models/fraud_model.pkl')
    print("💾 Model saved to backend/models/fraud_model.pkl")

if __name__ == "__main__":
    train_and_select_best_model()
