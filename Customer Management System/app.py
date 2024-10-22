# app.py

import streamlit as st
from backend import authenticate_user
from main import add_customer_ui, view_customers_ui, update_customer_ui, delete_customer_ui

# User Authentication
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.sidebar.success(f"Logged in as {username}")
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            return True
        else:
            st.sidebar.error("Invalid username or password")
            st.session_state['authenticated'] = False
    return False

# Main function to control the Streamlit app
def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        login_successful = login()
        if not login_successful:
            return

    if st.session_state['authenticated']:
        st.sidebar.title("Navigation")
        menu = ["Add Customer", "View Customers", "Update Customer", "Delete Customer"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Add Customer":
            add_customer_ui()
        elif choice == "View Customers":
            view_customers_ui()
        elif choice == "Update Customer":
            update_customer_ui()
        elif choice == "Delete Customer":
            delete_customer_ui()

if __name__ == "__main__":
    main()
