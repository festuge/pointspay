import os
import mysql.connector
from mysql.connector import Error

# Retrieve environment variables for database connection
db_endpoint = os.getenv("DB_ENDPOINT")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Print the retrieved values (for debugging purposes, remove in production)
print(f"Connecting to database: {db_name}")
print(f"Endpoint: {db_endpoint}, Username: {db_username}")

try:
    # Establish a connection to the database
    connection = mysql.connector.connect(
        host=db_endpoint,
        user=db_username,
        password=db_password,
        database=db_name
    )

    if connection.is_connected():
        print("Connection successful!")
        db_info = connection.get_server_info()
        print(f"Connected to MySQL Server version: {db_info}")

        # Test a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"You're connected to database: {record[0]}")

        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Database connection closed.")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")