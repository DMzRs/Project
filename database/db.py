import mysql.connector
from mysql.connector import Error
import streamlit as st
import hashlib

DB_CONFIG = {
    "host": st.secrets["mysql"]["host"],
    "port": st.secrets["mysql"]["port"],
    "database": st.secrets["mysql"]["database"],
    "user": st.secrets["mysql"]["user"],
    "password": st.secrets["mysql"]["password"]
}


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None


def add_ingredient(name, category, price, stock_quantity, overall_price):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO ingredients (name, category, price, stock_quantity, overall_price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, category, price,
                           stock_quantity, overall_price))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            st.error(f"Error inserting ingredient: {e}")
            return False
    return False


def get_all_ingredients():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ingredients")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            st.error(f"Error fetching ingredients: {e}")
            return []
    return []


def update_ingredient_stock(ingredient_id, new_price, new_quantity, new_overall_price):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                UPDATE ingredients
                SET price=%s, stock_quantity=%s, overall_price=%s
                WHERE ingredient_id=%s
            """
            cursor.execute(
                query, (new_price, new_quantity, new_overall_price, ingredient_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            st.error(f"Error updating ingredient: {e}")
            return False
    return False


def search_ingredients_by_name(name):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM ingredients WHERE name LIKE %s"
            cursor.execute(query, (f"%{name}%",))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            st.error(f"Error searching ingredients: {e}")
            return []
    return []


# ----------- User Management Functions -----------#

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, password, firstname, lastname):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        hashed = hash_password(password)

        query = """
            INSERT INTO users (username, password, first_name, last_name)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, hashed, firstname, lastname))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Error as e:
        st.error(f"Error creating user: {e}")
        return False


def authenticate(username, password):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        hashed = hash_password(password)

        cursor.execute("SELECT user_id, first_name FROM users WHERE username=%s AND password=%s",
                       (username, hashed))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return user  # None if wrong login
    except Error as e:
        st.error(f"Login error: {e}")
        return None


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def update_user_profile(user_id, username, firstname, lastname):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            UPDATE users 
            SET username = %s, first_name = %s, last_name = %s
            WHERE user_id = %s
        """
        cursor.execute(query, (username, firstname, lastname, user_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()


def update_user_password(user_id, old_pass, new_pass):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Check old password
    cursor.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    if not result or result["password"] != old_pass:
        return False  # Incorrect current password

    # Update new password
    cursor.execute(
        "UPDATE users SET password = %s WHERE user_id = %s",
        (new_pass, user_id),
    )
    conn.commit()

    cursor.close()
    conn.close()
    return True
