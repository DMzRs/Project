import streamlit as st
import database.db as db

st.title("Update Burger Ingredient")
db.get_connection()

# --- Update Ingredient function ---


def reset_fields():
    st.session_state["ingredient_name"] = ""
    st.session_state["ingredient_quantity"] = 0
    st.session_state["ingredient_price"] = 0.0
    st.session_state["ingredient_category"] = "Vegetable"


def update_ingredient():
    name = st.session_state["ingredient_name"]
    new_qty = st.session_state["new_ingredient_quantity"]
    new_price = st.session_state["new_ingredient_price"]
    cat = st.session_state["ingredient_category"]

    # Validation
    if not name:
        st.error("Please enter an ingredient name!")
        return
    if new_qty == 0:
        st.warning("Quantity should be greater than 0")
        return
    if new_price == 0.0:
        st.warning("Price should be greater than 0")
        return

    overall_price = new_qty * new_price

    ingredients = db.get_all_ingredients()
    ingredient_found = False
    for ingredient in ingredients:
        if ingredient['name'].lower() == name.lower():
            ingredient_found = True
            success = db.update_ingredient_stock(
                ingredient['ingredient_id'], new_price, new_qty, overall_price)
            if success:
                st.success(f"Successfully updated **{name}**!")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Ingredient", name)
                with col2:
                    st.metric("Category", cat)
                with col3:
                    st.metric("Quantity", f"{new_qty} units")
                with col4:
                    st.metric("Price/Unit", f"${new_price:.2f}")
                with col5:
                    st.metric("Total Value",
                              f"${overall_price:.2f}")
            else:
                st.error(f"Failed to update **{name}**.")
            break

    if not ingredient_found:
        st.error(f"Ingredient **{name}** not found in the database.")

    reset_fields()


# ---Inputs---
st.text_input("Ingredient Name", key="ingredient_name")
st.number_input("New Quantity", min_value=0, step=1,
                key="new_ingredient_quantity")
st.number_input("New Price per Unit", min_value=0.0,
                step=0.01, key="new_ingredient_price")
st.selectbox("Ingredient Category", [
             "Vegetable", "Cheese", "Meat", "Sauce"], key="ingredient_category")

st.button("Update Ingredient", on_click=update_ingredient)
