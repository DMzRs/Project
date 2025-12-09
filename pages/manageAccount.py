import streamlit as st
import database.db as db

st.title("Manage Your Account")

# ---------------------------------------------------
# Check Login Status
# ---------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in to access this page.")
    st.stop()

user_id = st.session_state["user_id"]
firstname = st.session_state["firstname"]

st.subheader(f"Hello, {firstname}! 👋")
st.write("Manage your account details below.")

# ---------------------------------------------------
# Fetch current user data from DB
# ---------------------------------------------------
user_data = db.get_user_by_id(user_id)

if not user_data:
    st.error("Unable to load user information.")
    st.stop()

current_username = user_data["username"]
current_firstname = user_data["first_name"]
current_lastname = user_data["last_name"]

# ---------------------------------------------------
# Update Profile
# ---------------------------------------------------
st.header("Update Profile Information")

with st.form("update_profile_form"):
    new_username = st.text_input("Username", value=current_username)
    new_firstname = st.text_input("First Name", value=current_firstname)
    new_lastname = st.text_input("Last Name", value=current_lastname)

    update_profile_btn = st.form_submit_button("Update Profile")

if update_profile_btn:
    result = db.update_user_profile(
        user_id,
        new_username,
        new_firstname,
        new_lastname
    )

    if result:
        st.success("Profile updated successfully!")
        st.session_state["firstname"] = new_firstname
        st.rerun()
    else:
        st.error("Failed to update profile. Username may already exist.")


# ---------------------------------------------------
# Update Password
# ---------------------------------------------------
st.header("Change Password")

with st.form("password_form"):
    old_pass = st.text_input("Current Password", type="password")
    new_pass = st.text_input("New Password", type="password")

    change_pass_btn = st.form_submit_button("Update Password")

if change_pass_btn:
    result = db.update_user_password(user_id, old_pass, new_pass)

    if result:
        st.success("Password updated successfully!")
    else:
        st.error("Incorrect old password.")


# ---------------------------------------------------
# Logout Button
# ---------------------------------------------------
st.header("Logout")

if st.button("Logout"):
    st.session_state.clear()
    st.success("You have been logged out.")
    st.rerun()
