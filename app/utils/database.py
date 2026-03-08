import mysql.connector
from mysql.connector import Error
from app.config.settings import settings
import streamlit as st

class Database:
    def __init__(self):
        self.connection = None
        
    def create_connection(self):
        """Create database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD
            )
            return self.connection
        except Error as e:
            st.error(f"Database connection error: {e}")
            return None
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute SQL query"""
        conn = self.create_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
            
            cursor.close()
            conn.close()
            return result
        except Error as e:
            st.error(f"Query execution error: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        query = "SELECT * FROM users WHERE Email = %s"
        return self.execute_query(query, (email,), fetch=True)
    
    def create_user(self, name, email, password_hash):
        """Create new user"""
        query = "INSERT INTO users (Name, Email, password_hash) VALUES (%s, %s, %s)"
        return self.execute_query(query, (name, email, password_hash))
    
    def get_stock_symbols(self):
        """Get all stock symbols"""
        query = "SELECT * FROM symbols"
        return self.execute_query(query, fetch=True)
    
    def get_stock_prices(self, symbol_id, limit=100):
        """Get stock prices"""
        query = """
            SELECT * FROM prices 
            WHERE Symbol_ID = %s 
            ORDER BY Date DESC 
            LIMIT %s
        """
        return self.execute_query(query, (symbol_id, limit), fetch=True)
    
    def save_prediction(self, symbol_id, user_id, model_type, 
                       prediction_value, confidence, trend, notes=""):
        """Save prediction to database"""
        query = """
            INSERT INTO prediction 
            (Symbol_ID, User_ID, Model_type, Prediction_value, Confidence, Trend, Notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (symbol_id, user_id, model_type, 
                                         prediction_value, confidence, trend, notes))
    
    def save_trade(self, user_id, symbol_id, action, price, quantity):
        """Save simulated trade"""
        query = """
            INSERT INTO trade_sims 
            (User_id, Symbol_id, Action, Price, Quantity)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (user_id, symbol_id, action, price, quantity))
    
    def get_user_trades(self, user_id):
        """Get user's trade history"""
        query = """
            SELECT ts.*, s.Code, s.Name 
            FROM trade_sims ts
            JOIN symbols s ON ts.Symbol_id = s.Symbol_ID
            WHERE ts.User_id = %s
            ORDER BY ts.Timestamp DESC
        """
        return self.execute_query(query, (user_id,), fetch=True)
    
    def get_user_predictions(self, user_id, limit=50):
        """Get user's prediction history"""
        query = """
            SELECT p.*, s.Code, s.Name 
            FROM prediction p
            JOIN symbols s ON p.Symbol_ID = s.Symbol_ID
            WHERE p.User_ID = %s
            ORDER BY p.Date_time DESC
            LIMIT %s
        """
        return self.execute_query(query, (user_id, limit), fetch=True)

db = Database()