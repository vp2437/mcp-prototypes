from mcp.server.fastmcp import FastMCP
import sqlite3, json
import os

mcp = FastMCP("SQL Server")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_conn():
    return sqlite3.connect(DB_PATH)

@mcp.tool()
def server_directory():
    """
    Return the directory containing server.py.
    Useful for debugging file path issues.
    """
    return BASE_DIR


@mcp.tool()
def list_database_files():
    """
    List all SQLite database files located beside server.py.
    """
    return [f for f in os.listdir(BASE_DIR) if f.lower().endswith(".db")]

@mcp.tool()
def run_query(sql: str) -> str:
    """
    Execute a SELECT query against the SQLite database.

    Use this tool when a user wants to:
    - retrieve records
    - search data
    - generate reports
    - analyze business data

    Only use SELECT statements.

    Args:
        sql: SQL SELECT query.

    Returns:
        Query results in JSON format.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    cols = [d[0] for d in cursor.description]
    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    conn.close()
    return json.dumps(rows, indent=2)

@mcp.tool()
def run_write(sql: str) -> str:
    """
    Execute INSERT, UPDATE, or DELETE statements.

    Use this tool when a user wants to modify database records.

    Args:
        sql: SQL write statement.

    Returns:
        Confirmation message.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return f"Query executed. Rows affected: {affected}"

@mcp.tool()
def list_tables() -> str:
    """
    List all tables available in the SQLite database.

    Use this tool before generating SQL queries
    when the database structure is unknown.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cursor.fetchall()]
    conn.close()
    return json.dumps(tables)

@mcp.tool()
def describe_table(table_name: str) -> str:
    """
    Show column names and data types for a table.

    Use this tool before querying a table
    to understand its schema.

    Args:
        table_name: Name of the table.

    Returns:
        Table schema as JSON.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = cursor.fetchall()
    conn.close()
    return json.dumps([{"col": c[1], "type": c[2]} for c in cols], indent=2)

@mcp.tool()
def seed_demo_data() -> str:
    """Create and populate a demo 'orders' table for testing."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer TEXT,
            product TEXT,
            quantity INTEGER,
            date TEXT
        )
    """)
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", [
        (1, "Alice", "Laptop", 1, "2024-06-01"),
        (2, "Bob", "Mouse", 3, "2024-06-03"),
        (3, "Alice", "Keyboard", 2, "2024-06-10"),
        (4, "Charlie", "Monitor", 1, "2024-06-15"),
    ])
    conn.commit()
    conn.close()
    return "Demo orders table created and seeded."

if __name__ == "__main__":
    mcp.run(transport="stdio")