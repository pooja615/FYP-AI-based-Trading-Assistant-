import streamlit as st
from app.utils.auth import check_authentication, logout_user, hash_password
from app.utils.database import db

def settings_page():
    st.set_page_config(page_title="TradeSync - Settings", page_icon="⚙️")
    
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
    st.markdown("<h1>⚙️ Settings</h1>", unsafe_allow_html=True)
    
    # Profile Settings
    st.markdown("### 👤 Profile Settings")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=st.session_state.user_name)
        with col2:
            email = st.text_input("Email", value=st.session_state.user_email, disabled=True)
        
        if st.form_submit_button("Update Profile"):
            st.info("Profile update functionality coming soon!")
    
    st.markdown("---")
    
    # Password Change
    st.markdown("### 🔐 Change Password")
    
    with st.form("password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Change Password"):
            if new_password != confirm_password:
                st.error("New passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                st.info("Password change functionality coming soon!")
    
    st.markdown("---")
    
    # Theme Settings
    st.markdown("### 🎨 Theme Settings")
    
    theme = st.selectbox("Select Theme", ["Light", "Dark", "Auto"])
    st.info(f"Current theme: {theme}")
    
    st.markdown("---")
    
    # About
    st.markdown("### ℹ️ About TradeSync")
    
    st.markdown("""
    **TradeSync** is an AI-Based Trading Assistant designed for educational purposes.
    
    **Version:** 1.0.0  
    **Developer:** Pooja Kumari Yadav  
    **Student ID:** 23056290  
    **Module:** CS6P05NI Final Year Project  
    **Institution:** Islington College / London Metropolitan University
    
    **Disclaimer:** This platform is for educational purposes only. 
    Do not use for real trading decisions.
    """)

if __name__ == "__main__":
    settings_page()