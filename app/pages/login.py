import streamlit as st
from app.utils.auth import login_user

def login_page():
    st.set_page_config(page_title="TradeSync - Login", page_icon="📈")
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
        }
        .login-container {
            padding: 2rem;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📈 TradeSync</h1>", 
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>AI-Based Trading Assistant</h3>", 
                unsafe_allow_html=True)
    
    # Login Form
    with st.form("login_form"):
        st.markdown("### Login to Your Account")
        
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submit = st.form_submit_button("Login")
        with col2:
            if st.form_submit_button("Register"):
                st.switch_page("app/pages/register.py")
        
        if submit:
            if email and password:
                success, result = login_user(email, password)
                
                if success:
                    st.success(f"Welcome back, {result['Name']}!")
                    st.session_state.authenticated = True
                    st.switch_page("app/pages/dashboard.py")
                else:
                    st.error(result)
            else:
                st.warning("Please fill in all fields")
    
    # Demo Credentials
    with st.expander("📝 Demo Credentials"):
        st.write("**Email:** user@tradesync.com")
        st.write("**Password:** admin123")

if __name__ == "__main__":
    login_page()