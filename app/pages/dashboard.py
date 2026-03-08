import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.utils.auth import check_authentication, logout_user
from app.utils.database import db

def dashboard_page():
    st.set_page_config(page_title="TradeSync - Dashboard", page_icon="📈", layout="wide")
    
    # Check authentication
    if not check_authentication():
        st.switch_page("app/pages/login.py")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.markdown(f"📧 {st.session_state.user_email}")
        st.markdown("---")
        
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
    
    # Main Dashboard
    st.markdown("<h1>📈 Trading Dashboard</h1>", unsafe_allow_html=True)
    
    # Get stock symbols
    symbols = db.get_stock_symbols()
    
    if symbols:
        # Top Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Available Stocks", len(symbols))
        with col2:
            st.metric("Your Trades", len(db.get_user_trades(st.session_state.user_id)) if st.session_state.user_id else 0)
        with col3:
            st.metric("Predictions Made", len(db.get_user_predictions(st.session_state.user_id)) if st.session_state.user_id else 0)
        with col4:
            st.metric("Portfolio Value", "Rs. 100,000")  # Simulated
        
        st.markdown("---")
        
        # Stock Selection
        col1, col2 = st.columns([3, 1])
        
        with col1:
            stock_options = {f"{s['Code']} - {s['Name']}": s['Symbol_ID'] for s in symbols}
            selected_stock = st.selectbox("Select Stock", list(stock_options.keys()))
        
        with col2:
            st.markdown("### Quick Actions")
            if st.button("🔮 Get Prediction"):
                st.switch_page("app/pages/prediction.py")
            if st.button("💰 Make Trade"):
                st.switch_page("app/pages/portfolio.py")
        
        # Stock Info
        if selected_stock:
            symbol_id = stock_options[selected_stock]
            symbol_info = [s for s in symbols if s['Symbol_ID'] == symbol_id][0]
            
            st.markdown(f"### {symbol_info['Code']} - {symbol_info['Name']}")
            st.markdown(f"**Sector:** {symbol_info.get('sector', 'N/A')} | **Exchange:** {symbol_info['Exchange']}")
            
            # Get prices
            prices = db.get_stock_prices(symbol_id)
            
            if prices:
                # Create DataFrame
                df = pd.DataFrame(prices)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')
                
                # Price Chart
                fig = go.Figure()
                fig.add_trace(go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Price'
                ))
                fig.update_layout(
                    title=f"{symbol_info['Code']} Price Chart",
                    xaxis_title='Date',
                    yaxis_title='Price (Rs.)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Price Stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Current Price", f"Rs. {df['Close'].iloc[-1]:.2f}")
                with col2:
                    st.metric("Day High", f"Rs. {df['High'].iloc[-1]:.2f}")
                with col3:
                    st.metric("Day Low", f"Rs. {df['Low'].iloc[-1]:.2f}")
                with col4:
                    change = ((df['Close'].iloc[-1] - df['Open'].iloc[-1]) / df['Open'].iloc[-1]) * 100
                    st.metric("Day Change", f"{change:.2f}%", delta_color="normal")
            else:
                st.warning("No price data available for this stock")
    else:
        st.warning("No stocks available. Please add stock data to the database.")
    
    # Recent Activity
    st.markdown("---")
    st.markdown("### 📊 Recent Activity")
    
    predictions = db.get_user_predictions(st.session_state.user_id, limit=5)
    
    if predictions:
        pred_df = pd.DataFrame(predictions)
        st.dataframe(pred_df[['Code', 'Name', 'Prediction_value', 'Trend', 'Confidence', 'Date_time']], 
                    use_container_width=True)
    else:
        st.info("No recent predictions. Get started by making a prediction!")

if __name__ == "__main__":
    dashboard_page()