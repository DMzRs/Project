import streamlit as st
import database.db as db

st.title("Add Burger Ingredient")

db.get_connection()

# --- Reset function ---


def reset_fields():
    st.session_state["ingredient_name"] = ""
    st.session_state["ingredient_quantity"] = 0
    st.session_state["ingredient_price"] = 0.0
    st.session_state["ingredient_category"] = "Vegetable"

# --- Add Ingredient function ---


def add_ingredient():
    name = st.session_state["ingredient_name"]
    qty = st.session_state["ingredient_quantity"]
    price = st.session_state["ingredient_price"]
    cat = st.session_state["ingredient_category"]

    # Validation
    if not name:
        st.error("Please enter an ingredient name!")
        return
    if qty == 0:
        st.warning("Quantity should be greater than 0")
        return
    if price == 0.0:
        st.warning("Price should be greater than 0")
        return

    overall_price = qty * price
    new_ingredient = db.add_ingredient(name, cat, price, qty, overall_price)
    st.success(f"Successfully added **{name}**!")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Ingredient", name)
    with col2:
        st.metric("Category", cat)
    with col3:
        st.metric("Quantity", f"{qty} units")
    with col4:
        st.metric("Price/Unit", f"${price:.2f}")
    with col5:
        st.metric("Total Value",
                  f"${overall_price:.2f}")

    # Reset fields AFTER success
    reset_fields()


# ---Inputs---
st.text_input("Ingredient Name", key="ingredient_name")
st.number_input("Quantity", min_value=0, step=1, key="ingredient_quantity")
st.number_input("Price per Unit", min_value=0.0, format="%.2f",
                step=0.01, key="ingredient_price")
st.selectbox("Category",
             ["Vegetable", "Meat", "Dairy", "Grain", "Other"],
             key="ingredient_category")

st.button("Add Ingredient", on_click=add_ingredient)
