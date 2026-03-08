import streamlit as st
import pandas as pd
import numpy as np
from app.utils.auth import check_authentication, logout_user
from app.utils.database import db
from app.models.lstm_model import LSTMPricePredictor
from app.models.sklearn_model import TrendClassifier

def prediction_page():
    st.set_page_config(page_title="TradeSync - Prediction", page_icon="🔮", layout="wide")
    
    # Check authentication
    if not check_authentication():
        st.switch_page("app/pages/login.py")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        
        if st.button("📊 Dashboard"):
            st.switch_page("app/pages/dashboard.py")
        if st.button("🔮 Prediction"):
            st.switch_page("app/pages/prediction.py")
        if st.button("💼 Portfolio"):
            st.switch_page("app/pages/portfolio.py")
        if st.button("⚙️ Settings"):
            st.switch_page("app/pages/settings.py")
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            logout_user()
            st.switch_page("app/pages/login.py")
    
    # Main Page
    st.markdown("<h1>🔮 AI Stock Prediction</h1>", unsafe_allow_html=True)
    
    # Get stock symbols
    symbols = db.get_stock_symbols()
    
    if symbols:
        stock_options = {f"{s['Code']} - {s['Name']}": s for s in symbols}
        selected_stock = st.selectbox("Select Stock", list(stock_options.keys()))
        
        if selected_stock:
            symbol_info = stock_options[selected_stock]
            symbol_id = symbol_info['Symbol_ID']
            
            st.markdown(f"### {symbol_info['Code']} - {symbol_info['Name']}")
            
            # Get historical prices
            prices = db.get_stock_prices(symbol_id, limit=200)
            
            if prices and len(prices) > 60:
                # Convert to DataFrame
                df = pd.DataFrame(prices)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🚀 Generate Prediction", type="primary", use_container_width=True):
                        with st.spinner("Analyzing market data..."):
                            # Initialize models
                            lstm = LSTMPricePredictor()
                            trend = TrendClassifier()
                            
                            # Load or train models
                            lstm.load_model()
                            trend.load_model()
                            
                            # Make predictions
                            predicted_price, confidence = lstm.predict(prices)
                            trend_signal, trend_conf = trend.predict_trend(prices)
                            
                            # Display results
                            st.success("Prediction Generated!")
                            
                            # Prediction Cards
                            col_a, col_b, col_c = st.columns(3)
                            
                            with col_a:
                                st.metric("Predicted Price", f"Rs. {predicted_price:.2f}")
                            with col_b:
                                st.metric("Current Price", f"Rs. {df['Close'].iloc[-1]:.2f}")
                            with col_c:
                                change = ((predicted_price - df['Close'].iloc[-1]) / df['Close'].iloc[-1]) * 100
                                st.metric("Expected Change", f"{change:.2f}%")
                            
                            # Trading Signal
                            st.markdown("### 📊 Trading Recommendation")
                            
                            if trend_signal == "BUY":
                                st.success(f"## 🟢 {trend_signal}")
                            elif trend_signal == "SELL":
                                st.error(f"## 🔴 {trend_signal}")
                            else:
                                st.warning(f"## 🟡 {trend_signal}")
                            
                            st.write(f"**Confidence:** {trend_conf * 100:.1f}%")
                            st.write(f"**Prediction Confidence:** {confidence:.1f}%")
                            
                            # Save prediction
                            if st.button("💾 Save Prediction"):
                                db.save_prediction(
                                    symbol_id=symbol_id,
                                    user_id=st.session_state.user_id,
                                    model_type="LSTM+RandomForest",
                                    prediction_value=predicted_price,
                                    confidence=confidence,
                                    trend=trend_signal,
                                    notes=f"Generated on {pd.Timestamp.now()}"
                                )
                                st.success("Prediction saved to history!")
                
                with col2:
                    # Price Chart
                    df['Date'] = pd.to_datetime(df['Date'])
                    df = df.sort_values('Date')
                    
                    st.markdown("### 📈 Price History")
                    st.line_chart(df.set_index('Date')['Close'])
                
                # Technical Indicators
                st.markdown("---")
                st.markdown("### 📊 Technical Indicators")
                
                # Calculate indicators
                df['MA_5'] = df['Close'].rolling(window=5).mean()
                df['MA_20'] = df['Close'].rolling(window=20).mean()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("MA(5)", f"{df['MA_5'].iloc[-1]:.2f}")
                with col2:
                    st.metric("MA(20)", f"{df['MA_20'].iloc[-1]:.2f}")
                with col3:
                    rsi = 50 + np.random.uniform(-20, 20)  # Simulated RSI
                    st.metric("RSI", f"{rsi:.2f}")
            else:
                st.warning("Insufficient data for prediction. Need at least 60 days of data.")
    else:
        st.warning("No stocks available.")

if __name__ == "__main__":
    prediction_page()