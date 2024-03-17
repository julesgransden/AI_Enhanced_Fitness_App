import mysql.connector as sql
import streamlit as st

db = sql.connect(
    host="localhost",
    user="root",
    password="Beliveau1!",
    database="giraffe"
)

def authenticate(username, password):
    cursor = db.cursor()
    # Query the database to check if the entered username and password match
    query = "SELECT * FROM persoInfo WHERE username = %s AND pass = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False



