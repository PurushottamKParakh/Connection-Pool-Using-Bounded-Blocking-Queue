from ConnectionPool import ConnectionPool

if __name__ == "__main__":
    pool = ConnectionPool(max_size=3, host="localhost", user="admin", password="password", database="world")

    try:
        # Acquire connection
        conn = pool.acquire()

        # Execute a query
        conn.execute("SHOW TABLES;")

        # Release connection back to the pool
        pool.release(conn)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Shutdown the pool
        pool.shutdown()
