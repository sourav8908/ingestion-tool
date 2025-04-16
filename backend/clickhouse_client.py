from clickhouse_connect import get_client
from clickhouse_connect.driver.exceptions import ClickHouseError

def connect_clickhouse(host, port, database, username, jwt_token, secure=True):
    """
    Connects to ClickHouse using provided credentials.
    """
    try:
        client = get_client(
            host=host,
            port=int(port),
            username=username,
            password=jwt_token,
            database=database,
            secure=secure  # True for HTTPS, False for HTTP
        )
        return client
    except ClickHouseError as e:
        raise RuntimeError(f"ClickHouse connection failed: {str(e)}")


def fetch_tables(client):
    """
    Fetches a list of all table names in the connected ClickHouse database.
    """
    try:
        query = "SHOW TABLES"
        result = client.query(query)
        return [row[0] for row in result.result_rows]
    except Exception as e:
        raise RuntimeError(f"Failed to fetch tables: {str(e)}")


def fetch_columns(client, table_name):
    """
    Fetches column names of the specified table.
    """
    try:
        query = f"DESCRIBE TABLE {table_name}"
        result = client.query(query)
        return [row[0] for row in result.result_rows]  # Only column names
    except Exception as e:
        raise RuntimeError(f"Failed to fetch columns: {str(e)}")


def fetch_data_from_table(client, table_name):
    """
    Fetches all data from the specified table.
    """
    try:
        query = f"SELECT * FROM {table_name}"
        result = client.query(query)
        return result.result_rows
    except Exception as e:
        raise RuntimeError(f"Failed to fetch data: {str(e)}")
