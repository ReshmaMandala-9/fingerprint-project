import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change if needed
        password="23BQ1A05D2",      # your MySQL password
        database="fingerprint_db"
    )