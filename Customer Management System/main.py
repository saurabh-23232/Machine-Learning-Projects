# main.py

import streamlit as st
from backend import add_customer, view_customers, update_customer, delete_customer, get_customer_by_id

# Add a new customer
def add_customer_ui():
    st.title("Add New Customer")

    with st.form("customer_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        address = st.text_area("Address")
        city = st.text_input("City")
        state = st.text_input("State")
        postal_code = st.text_input("Postal Code")
        country = st.text_input("Country")

        submitted = st.form_submit_button("Add Customer")
        
        if submitted:
            if first_name and last_name and email:
                try:
                    add_customer(first_name, last_name, email, phone_number, address, city, state, postal_code, country)
                    st.success("Customer added successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please fill in all required fields (First Name, Last Name, Email).")

# View all customers
def view_customers_ui():
    st.title("Customer List")
    customers = view_customers()
    if customers:
        for customer in customers:
            st.write(f"ID: {customer[0]}, Name: {customer[1]} {customer[2]}, Email: {customer[3]}, Phone: {customer[4]}")
    else:
        st.write("No customers found.")

# Update a customer
def update_customer_ui():
    st.title("Update Customer")
    customer_id = st.text_input("Customer ID")
    if customer_id:
        customer = get_customer_by_id(customer_id)
        if customer:
            first_name = st.text_input("First Name", value=customer[1])
            last_name = st.text_input("Last Name", value=customer[2])
            email = st.text_input("Email", value=customer[3])
            phone_number = st.text_input("Phone Number", value=customer[4])
            address = st.text_area("Address", value=customer[5])
            city = st.text_input("City", value=customer[6])
            state = st.text_input("State", value=customer[7])
            postal_code = st.text_input("Postal Code", value=customer[8])
            country = st.text_input("Country", value=customer[9])
            
            if st.button("Update Customer"):
                update_customer(customer_id, first_name, last_name, email, phone_number, address, city, state, postal_code, country)
                st.success("Customer updated successfully!")
        else:
            st.error("Customer not found.")

# Delete a customer
def delete_customer_ui():
    st.title("Delete Customer")
    customer_id = st.text_input("Customer ID")
    
    if st.button("Delete Customer"):
        delete_customer(customer_id)
        st.warning("Customer deleted!")
