import streamlit as st

def main():
    st.set_page_config(
        page_title="TradeSync",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Redirect to login
    st.switch_page("app/pages/login.py")

if __name__ == "__main__":
    main()