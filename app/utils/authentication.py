import bcrypt
import streamlit as st

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def login_user(email, password):
    """Login user"""
    from app.utils.database import db
    
    user = db.get_user_by_email(email)
    
    if user and len(user) > 0:
        user = user[0]
        if verify_password(password, user['password_hash']):
            st.session_state.authenticated = True
            st.session_state.user_id = user['User_ID']
            st.session_state.user_name = user['Name']
            st.session_state.user_email = user['Email']
            st.session_state.user_role = user['role']
            return True, user
        else:
            return False, "Invalid password"
    else:
        return False, "User not found"

def logout_user():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None
    st.session_state.user_role = None