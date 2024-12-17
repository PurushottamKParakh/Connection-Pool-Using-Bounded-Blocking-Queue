import mysql.connector
from mysql.connector import Error
import threading
import queue


class Connection:
    """Represents a MySQL connection with query execution and lifecycle management."""

    def __init__(self, connection_id, db_connection):
        """
        Initialize a MySQL connection wrapper.

        Args:
            connection_id (int): Unique identifier for the connection.
            db_connection: MySQL database connection object.
        """
        self.connection_id = connection_id
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()

    def execute(self, query):
        """
        Executes a SQL query and prints results.

        Args:
            query (str): The SQL query to execute.
        """
        try:
            print(f"[Connection {self.connection_id}] Executing query: {query}")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(f"[Connection {self.connection_id}] Error executing query: {e}")

    def close(self):
        """Closes the MySQL connection."""
        try:
            print(f"[Connection {self.connection_id}] Closing connection.")
            self.cursor.close()
            self.db_connection.close()
        except Error as e:
            print(f"[Connection {self.connection_id}] Error closing connection: {e}")

