import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ml.data_loader import fetch_data
from ml.features import add_features

def train_model(symbol="BTC/USD"):
    df = fetch_data(symbol)
    df = add_features(df)
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)
    
    X = df.drop(columns=["target", "open", "high", "low", "close", "volume"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    joblib.dump(model, "backend/ml/model.pkl")
    return model

if __name__ == "__main__":
    train_model()
