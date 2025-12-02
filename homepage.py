import streamlit as st

st.logo("assets/logo.jpg")

pages = {
    "Your account": [
        st.Page("pages/createAccount.py", title="Create your account"),
        st.Page("pages/manageAccount.py", title="Manage your account"),
    ],

    "Menu": [
        st.Page("pages/add.py", title="Add Burger Ingredient", icon="➕"),
        st.Page("pages/update.py", title="Update Burger Ingredient", icon="🔄"),
        st.Page("pages/view.py", title="View Burger Ingredient", icon="👁️"),

    ],
}

pg = st.navigation(pages)
pg.run()
