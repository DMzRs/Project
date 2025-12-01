import mysql.connector
from mysql.connector import Error
import streamlit as st

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
