import streamlit as st
from app.utils.auth import hash_password
from app.utils.database import db

def register_page():
    st.set_page_config(page_title="TradeSync - Register", page_icon="📈")
    
    # Custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📈 TradeSync</h1>", 
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Create Your Account</h3>", 
                unsafe_allow_html=True)
    
    # Registration Form
    with st.form("register_form"):
        st.markdown("### Register New Account")
        
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", 
                                        placeholder="Confirm your password")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submit = st.form_submit_button("Register")
        with col2:
            if st.form_submit_button("Login"):
                st.switch_page("app/pages/login.py")
        
        if submit:
            # Validation
            if not all([name, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                # Check if email exists
                existing_user = db.get_user_by_email(email)
                
                if existing_user and len(existing_user) > 0:
                    st.error("Email already registered")
                else:
                    # Create user
                    password_hash = hash_password(password)
                    user_id = db.create_user(name, email, password_hash)
                    
                    if user_id:
                        st.success("Account created successfully! Please login.")
                        st.switch_page("app/pages/login.py")
                    else:
                        st.error("Failed to create account")
    
    # Terms
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 12px;'>
        By registering, you agree to our Terms of Service and Privacy Policy.
        This is an educational platform for learning purposes only.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    register_page()