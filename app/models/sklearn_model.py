import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class TrendClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.model_path = 'app/models/saved/trend_model.pkl'
        self.scaler_path = 'app/models/saved/trend_scaler.pkl'
        
    def create_features(self, prices):
        """Create technical indicators as features"""
        df = pd.DataFrame(prices)
        
        # Moving Averages
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        
        # Volume Change
        df['Volume_Change'] = df['Volume'].pct_change()
        
        # Price Change
        df['Price_Change'] = df['Close'].pct_change()
        
        # Target: 1=UP, 0=HOLD, -1=DOWN
        df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1,
                               np.where(df['Close'].shift(-1) < df['Close'], -1, 0))
        
        return df.dropna()
    
    def train(self, prices):
        """Train the classifier"""
        df = self.create_features(prices)
        
        features = ['MA_5', 'MA_20', 'RSI', 'MACD', 'Volume_Change', 'Price_Change']
        X = df[features].values
        y = df['Target'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        return self.model.score(X_scaled, y)
    
    def load_model(self):
        """Load saved model"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        return False
    
    def predict_trend(self, prices):
        """Predict trend (BUY/SELL/HOLD)"""
        if self.model is None:
            if not self.load_model():
                return "HOLD", 0.5
        
        df = self.create_features(prices)
        
        features = ['MA_5', 'MA_20', 'RSI', 'MACD', 'Volume_Change', 'Price_Change']
        X = df[features].values[-1:].reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        confidence = max(probabilities)
        
        trend_map = {1: "BUY", -1: "SELL", 0: "HOLD"}
        return trend_map.get(prediction, "HOLD"), confidence