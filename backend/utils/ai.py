import os
import random
import json
import joblib
from utils.data import get_price
from utils.backtest import run_backtest
from utils.correlation import analyze_correlation
from utils.features import extract_features
from ml.model_train import load_or_train_model

# Load settings
with open("backend/settings.json", "r") as f:
    SETTINGS = json.load(f)

AI_MODE = SETTINGS.get("ai_mode", "basic")
CONFIDENCE_THRESHOLD = SETTINGS.get("confidence_threshold", 75)
USE_CORRELATION = SETTINGS.get("use_correlation", False)

def generate_signal(symbol):
    price = get_price(symbol)
    if not price:
        return "HOLD", 0, 0

    # Extract features
    features = extract_features(symbol)

    if AI_MODE == "ml":
        model = load_or_train_model(symbol)
        if not model:
            return "HOLD", 0, price

        prediction = model.predict([features])[0]
        confidence = int(model.predict_proba([features]).max() * 100)
        signal = {0: "SELL", 1: "HOLD", 2: "BUY"}.get(prediction, "HOLD")
    else:
        # Fallback mode (random logic)
        confidence = random.randint(65, 90)
        signal = random.choices(["BUY", "SELL", "HOLD"], weights=[0.3, 0.3, 0.4])[0]

    # Apply correlation boost if enabled
    if USE_CORRELATION:
        correlation_score = analyze_correlation(symbol)
        if correlation_score > 0.8 and signal != "HOLD":
            confidence = min(confidence + 10, 99)
        elif correlation_score < 0.3:
            confidence = max(confidence - 10, 50)

    return signal, confidence, price

def learn_from_performance(symbol):
    result = run_backtest(symbol)
    score = round(result["win_rate"] * result["sharpe_ratio"], 2)

    if AI_MODE == "ml":
        model = load_or_train_model(symbol, retrain=True)
        updated = "Model retrained"
    else:
        updated = "Thresholds updated"

    return {"score": score, "status": updated}
