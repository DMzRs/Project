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

selected_label = st.selectbox(
    "Select Ingredient to Delete",
    options=list(ingredient_map.keys())
)

selected_id = ingredient_map[selected_label]

# --- Delete action ---
if st.button("Delete Ingredient", type="primary"):
    success = db.delete_ingredient(selected_id)

    if success:
        st.success("Ingredient deleted successfully!")
        st.rerun()
    else:
        st.error("Failed to delete ingredient.")
