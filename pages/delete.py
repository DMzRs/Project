import streamlit as st
import database.db as db
import pandas as pd

st.title("Delete Burger Ingredient")

db.get_connection()

# --- Login check ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in to access this page.")
    st.stop()

# --- Fetch ingredients ---
ingredients = db.get_all_ingredients()

if not ingredients:
    st.info("No ingredients available.")
    st.stop()

# --- Convert to DataFrame ---
df = pd.DataFrame(ingredients)

st.subheader("Current Ingredients Inventory")
st.dataframe(
    df[[
        "ingredient_id",
        "name",
        "category",
        "price",
        "stock_quantity",
        "overall_price"
    ]],
    use_container_width=True
)

st.divider()

# --- Select ingredient to delete ---
ingredient_map = {
    f"{row['name']} ({row['category']}) - ID {row['ingredient_id']}": row["ingredient_id"]
    for _, row in df.iterrows()
}

ingredient_id = st.number_input(
    "Enter Ingredient ID",
    min_value=0,
    step=1
)

ingredient_name = st.text_input("Enter Ingredient Name")

selected_id = None
if ingredient_id > 0 and ingredient_name:
    for label, id_val in ingredient_map.items():
        if str(ingredient_id) in label and ingredient_name.lower() in label.lower():
            selected_id = id_val
            break

    if selected_id is None:
        st.warning("Ingredient not found. Please check the ID and name.")
        st.stop()

# --- Delete action ---
if st.button("Delete Ingredient", type="primary"):
    success = db.delete_ingredient(selected_id)

    if success:
        st.success("Ingredient deleted successfully!")
        st.rerun()
    else:
        st.error("Failed to delete ingredient.")
