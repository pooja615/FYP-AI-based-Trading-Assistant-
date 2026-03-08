import streamlit as st
import pandas as pd
from app.utils.auth import check_authentication, logout_user
from app.utils.database import db

def portfolio_page():
    st.set_page_config(page_title="TradeSync - Portfolio", page_icon="💼", layout="wide")
    
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
    st.markdown("<h1>💼 Simulated Portfolio</h1>", unsafe_allow_html=True)
    
    # Portfolio Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Initial Capital", "Rs. 100,000")
    with col2:
        trades = db.get_user_trades(st.session_state.user_id)
        total_trades = len(trades) if trades else 0
        st.metric("Total Trades", total_trades)
    with col3:
        if trades:
            total_pnl = sum([t['Profit_loss'] for t in trades])
            st.metric("Total P&L", f"Rs. {total_pnl:.2f}")
        else:
            st.metric("Total P&L", "Rs. 0.00")
    
    st.markdown("---")
    
    # Make Trade Section
    st.markdown("### 📝 Make a Trade")
    
    symbols = db.get_stock_symbols()
    
    if symbols:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            stock_options = {f"{s['Code']}": s for s in symbols}
            selected_stock = st.selectbox("Stock", list(stock_options.keys()))
        
        with col2:
            action = st.selectbox("Action", ["BUY", "SELL"])
        
        with col3:
            quantity = st.number_input("Quantity", min_value=1, value=10)
        
        with col4:
            if selected_stock:
                symbol_id = stock_options[selected_stock]['Symbol_ID']
                prices = db.get_stock_prices(symbol_id, limit=1)
                current_price = prices[0]['Close'] if prices else 0
                st.metric("Current Price", f"Rs. {current_price:.2f}")
        
        if st.button("Execute Trade", type="primary"):
            if selected_stock:
                symbol_id = stock_options[selected_stock]['Symbol_ID']
                prices = db.get_stock_prices(symbol_id, limit=1)
                price = prices[0]['Close'] if prices else 0
                
                trade_id = db.save_trade(
                    user_id=st.session_state.user_id,
                    symbol_id=symbol_id,
                    action=action,
                    price=price,
                    quantity=quantity
                )
                
                if trade_id:
                    st.success(f"Trade executed! Trade ID: {trade_id}")
                else:
                    st.error("Failed to execute trade")
    
    st.markdown("---")
    
    # Trade History
    st.markdown("### 📊 Trade History")
    
    trades = db.get_user_trades(st.session_state.user_id)
    
    if trades:
        trade_df = pd.DataFrame(trades)
        st.dataframe(trade_df[['Code', 'Name', 'Action', 'Price', 'Quantity', 
                               'Profit_loss', 'Timestamp']], use_container_width=True)
    else:
        st.info("No trades yet. Start trading to build your portfolio!")
    
    # Prediction History
    st.markdown("---")
    st.markdown("### 🔮 Prediction History")
    
    predictions = db.get_user_predictions(st.session_state.user_id)
    
    if predictions:
        pred_df = pd.DataFrame(predictions)
        st.dataframe(pred_df[['Code', 'Name', 'Prediction_value', 'Trend', 
                              'Confidence', 'Date_time']], use_container_width=True)
    else:
        st.info("No predictions yet. Get predictions from the Prediction page!")

if __name__ == "__main__":
    portfolio_page()