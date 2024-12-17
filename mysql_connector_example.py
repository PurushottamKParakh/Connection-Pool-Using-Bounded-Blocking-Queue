import mysql.connector

# Database configuration
config = {
    "host": "localhost",      # Change this to your MySQL server host
    "user": "admin",  # Your MySQL username
    "password": "password",  # Your MySQL password
    "database": "world"      # Database name you want to connect to
}
connection = None
cursor = None
try:
    # Establish connection
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Connected to the database.")

        # Create a cursor object
        cursor = connection.cursor()

        # Execute query to show tables
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        # Print tables
        print("Tables in the database:")
        for table in tables:
            print(table[0])

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed.")
