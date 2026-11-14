
import sqlite3
import time

from sqlalchemy import text

from src.database.connection import engine


# Maximum number of records returned
MAX_RESULT_ROWS = 500

# Maximum execution time in seconds
MAX_EXECUTION_SECONDS = 5

# Tables the agent is allowed to read
ALLOWED_TABLES = {"sales"}

# SQL functions permitted for analytics
ALLOWED_FUNCTIONS = {
    "count",
    "sum",
    "avg",
    "min",
    "max",
    "round",
    "lower",
    "upper",
    "length",
    "coalesce",
    "ifnull",
    "strftime"
}


def sqlite_authorizer(action, arg1, arg2, database, trigger):
    """
    Allow only approved database operations.
    """

    # Permit SELECT operations
    if action == sqlite3.SQLITE_SELECT:
        return sqlite3.SQLITE_OK

    # Permit reading only the sales table
    if action == sqlite3.SQLITE_READ:
        if arg1 in ALLOWED_TABLES:
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    # Permit only approved SQL functions
    if action == sqlite3.SQLITE_FUNCTION:
        function_name = (arg2 or arg1 or "").lower()

        if function_name in ALLOWED_FUNCTIONS:
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    # Permit recursive query processing
    if action == sqlite3.SQLITE_RECURSIVE:
        return sqlite3.SQLITE_OK

    # Permit only the cleanup PRAGMA operation
    if action == sqlite3.SQLITE_PRAGMA:
        pragma_name = (arg1 or "").lower()
        pragma_value = (arg2 or "").lower()

        if (
            pragma_name == "query_only"
            and pragma_value == "off"
        ):
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    # Reject all other operations
    return sqlite3.SQLITE_DENY


def execute_read_only_query(query: str):
    """
    Execute a restricted read-only SELECT query.

    Security controls:
    - SELECT statements only
    - Single SQL statement
    - Approved table access
    - Approved SQL functions
    - Maximum 500 returned records
    - Maximum 5 seconds of execution
    """

    # Step 1: Validate input
    if not query or not query.strip():
        raise ValueError("SQL query cannot be empty.")

    cleaned_query = query.strip()

    # Step 2: Allow only SELECT statements
    if not cleaned_query.upper().startswith("SELECT "):
        raise ValueError("Only SELECT queries are allowed.")

    # Step 3: Reject multiple SQL statements
    if ";" in cleaned_query.rstrip(";"):
        raise ValueError("Multiple SQL statements are not allowed.")

    connection = engine.connect()
    dbapi_connection = None

    try:
        # Step 4: Enable SQLite read-only query mode
        connection.exec_driver_sql("PRAGMA query_only = ON")

        # Access the underlying SQLite connection
        dbapi_connection = (
            connection.connection.driver_connection
        )

        # Step 5: Register the SQLite authorizer
        dbapi_connection.set_authorizer(sqlite_authorizer)

        # Step 6: Start execution-time monitoring
        start_time = time.monotonic()

        def query_timeout():
            elapsed = time.monotonic() - start_time
            return int(elapsed > MAX_EXECUTION_SECONDS)

        dbapi_connection.set_progress_handler(
            query_timeout,
            1000
        )

        # Step 7: Execute the query
        result = connection.execute(text(cleaned_query))

        # Step 8: Retrieve at most 501 records
        rows = result.fetchmany(MAX_RESULT_ROWS + 1)

        if len(rows) > MAX_RESULT_ROWS:
            raise ValueError(
                f"Query exceeded the maximum limit of "
                f"{MAX_RESULT_ROWS} records."
            )

        # Step 9: Convert results into dictionaries
        records = [
            dict(row._mapping)
            for row in rows
        ]

        return records

    finally:
        cleanup_successful = False

        try:
            if dbapi_connection is not None:

                # Remove execution-time monitoring
                dbapi_connection.set_progress_handler(None, 0)

                # Restore normal SQLite connection mode
                # The authorizer explicitly permits this operation
                dbapi_connection.execute(
                    "PRAGMA query_only = OFF"
                )

                # Remove the authorizer after cleanup
                dbapi_connection.set_authorizer(None)

            cleanup_successful = True

        finally:
            if cleanup_successful:
                connection.close()
            else:
                # Discard the connection if cleanup fails
                connection.invalidate()
                connection.close()
