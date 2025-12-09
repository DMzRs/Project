import streamlit as st
import database.db as db

st.title("View Ingredient Items")

# --- REQUIRE LOGIN ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in to access this page.")
    st.stop()

st.subheader("Filter Ingredients")

# --- CATEGORY FILTER ---
categories = ["All", "Vegetable", "Meat", "Dairy", "Grain", "Other"]
selected_category = st.selectbox("Select Category", categories)

# --- GET DATA FROM DATABASE ---
# Must return a list of dicts or tuples
ingredients = db.get_all_ingredients()

if not ingredients:
    st.info("No ingredients found.")
    st.stop()

# --- FILTER LOGIC ---
if selected_category != "All":
    ingredients = [
        item for item in ingredients if item["category"] == selected_category]

# --- DISPLAY TABLE ---
st.subheader("Ingredient List")

st.table(ingredients)
