import streamlit as st
import database.db as db

st.set_page_config(page_title="User Account", layout="centered")
st.title("User Account")

# Initialize session_state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


# --- PAGE SWITCHER ---
menu = st.sidebar.radio("Options", ["Login", "Signup"])

# -----------------------------------------------------------
# SIGNUP PAGE
# -----------------------------------------------------------
if menu == "Signup":
    st.subheader("Create Your Account")

    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        firstname = st.text_input("First Name")
        lastname = st.text_input("Last Name")

        submit = st.form_submit_button("Sign Up")

    if submit:
        if not username or not password or not firstname or not lastname:
            st.error("All fields are required!")
        else:
            result = db.create_user(username, password, firstname, lastname)

            if result:
                st.success("Account created successfully!")
            else:
                st.error("Failed to create account. Username may already exist.")


# -----------------------------------------------------------
# LOGIN PAGE
# -----------------------------------------------------------
elif menu == "Login":
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Login")

    if submit:
        user = db.authenticate(username, password)

        if user:
            user_id, firstname = user

            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id
            st.session_state["firstname"] = firstname

            st.success(f"Welcome back, {firstname}!")
            st.rerun()  # Refresh so session updates
        else:
            st.error("Invalid username or password")
