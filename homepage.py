import streamlit as st

st.logo("assets/logo.jpg")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


if st.session_state["logged_in"]:

    pages = {
        "Your account": [
            st.Page("pages/manageAccount.py", title="Manage your account"),
        ],

        "Menu": [
            st.Page("pages/add.py", title="Add Burger Ingredient", icon="➕"),
            st.Page("pages/update.py",
                    title="Update Burger Ingredient", icon="🔄"),
            st.Page("pages/view.py", title="View Burger Ingredient", icon="👁️"),
        ],
    }


else:

    pages = {
        "Your account": [
            st.Page("pages/createAccount.py", title="Create your account"),
        ],

        "Menu": [
            st.Page("pages/view.py", title="Please Login First ❗", icon="🔒"),
        ],
    }

pg = st.navigation(pages)
pg.run()
