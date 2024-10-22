# backend.py

import mysql.connector
import hashlib

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1454",
        database="CustomerManagementSystem"
    )

# Add a new customer
def add_customer(first_name, last_name, email, phone_number, address, city, state, postal_code, country):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO Customers (first_name, last_name, email, phone_number, address, city, state, postal_code, country)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (first_name, last_name, email, phone_number, address, city, state, postal_code, country))
    conn.commit()
    cursor.close()
    conn.close()

# View all customers
def view_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Update a customer's information
def update_customer(customer_id, first_name, last_name, email, phone_number, address, city, state, postal_code, country):
    conn = get_connection()
    cursor = conn.cursor()
    query = """UPDATE Customers SET first_name=%s, last_name=%s, email=%s, phone_number=%s, 
               address=%s, city=%s, state=%s, postal_code=%s, country=%s WHERE customer_id=%s"""
    cursor.execute(query, (first_name, last_name, email, phone_number, address, city, state, postal_code, country, customer_id))
    conn.commit()
    cursor.close()
    conn.close()

# Delete a customer
def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Customers WHERE customer_id=%s"
    cursor.execute(query, (customer_id,))
    conn.commit()
    cursor.close()
    conn.close()

# User authentication
def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    query = "SELECT * FROM Users WHERE username=%s AND password_hash=%s"
    cursor.execute(query, (username, password_hash))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Get customer by ID
def get_customer_by_id(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Customers WHERE customer_id=%s"
    cursor.execute(query, (customer_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data
