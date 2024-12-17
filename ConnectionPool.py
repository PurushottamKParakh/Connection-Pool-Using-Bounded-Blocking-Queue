import threading
import mysql
import mysql.connector
from mysql.connector import Error
import BlockingQueue
from Connection import Connection


class ConnectionPool:
    """A thread-safe MySQL connection pool."""

    def __init__(self, max_size=5, host="localhost", user="admin", password="password", database="world"):
        """
        Initializes the connection pool.

        Args:
            max_size (int): Maximum number of connections in the pool.
            host (str): MySQL server host.
            user (str): MySQL username.
            password (str): MySQL password.
            database (str): MySQL database name.
        """
        self.max_size = max_size
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._pool = BlockingQueue.BlockingQueue(max_size)
        self._lock = threading.Lock()
        self._initialize_pool()

    def _initialize_pool(self):
        """Pre-populates the pool with MySQL connections."""
        for i in range(self.max_size):
            connection = self._create_new_connection(i + 1)
            self._pool.enque(connection)

    def _create_new_connection(self, connection_id):
        """
        Creates a new MySQL connection.

        Args:
            connection_id (int): Unique identifier for the connection.

        Returns:
            Connection: A new MySQL connection object.
        """
        try:
            db_connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if db_connection.is_connected():
                print(f"[Connection {connection_id}] Established successfully.")
                return Connection(connection_id, db_connection)
        except Error as e:
            raise Exception(f"Error creating connection {connection_id}: {e}")

    def acquire(self, timeout=None):
        """
        Acquires a connection from the pool, blocking if necessary.

        Args:
            timeout (float): Time in seconds to wait before raising an exception.

        Returns:
            Connection: A connection object.
        """
        try:
            connection = self._pool.deque()
            print(f"Connection {connection.connection_id} acquired.")
            return connection
        except self._pool.empty():
            raise Exception("No available connections: Acquisition timeout.")

    def release(self, connection):
        """
        Returns a connection to the pool.

        Args:
            connection (Connection): The connection object to return.
        """
        if not isinstance(connection, Connection):
            raise ValueError("Invalid connection object.")
        with self._lock:
            print(f"Connection {connection.connection_id} released back to pool.")
            self._pool.enque(connection)

    def shutdown(self):
        """Closes all connections in the pool."""
        print("Shutting down connection pool...")
        while not self._pool.empty():
            connection = self._pool.deque()
            connection.close()
        print("Connection pool shutdown complete.")
