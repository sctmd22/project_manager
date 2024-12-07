from mysql.connector import Error, pooling


# Create a connection pool at the application level
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host="localhost",
    user="root",
    password="jqHRAK&WCK5iuQ4MP%",
    database="project_manager_db"
)


def db_connect():
    return connection_pool.get_connection()