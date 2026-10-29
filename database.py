import sqlite3
import data_cleaning

STORE_DB = '../data/store.db'

def get_connection(db_path: str = STORE_DB) -> sqlite3.Connection:
    """
    Open (and create, if needed) the SQLite database file.

    Returns:
        an open sqlite3.Connection

    """

    conn = sqlite3.connect(STORE_DB)
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    """
      Create the `products` and `sales` tables if they don't already exist. These have the following structure:

      products
        - product_id   TEXT, PRIMARY KEY
        - product_name TEXT, NOT NULL
        - category     TEXT
        - unit_price   REAL

      sales
        - sale_id        TEXT, PRIMARY KEY
        - product_id     TEXT, FOREIGN KEY references products(product_id)
        - quantity       INTEGER
        - sale_date      TEXT   (store as 'YYYY-MM-DD')
        - payment_method TEXT
        - customer_type  TEXT
    """

    conn.execute(
    """
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            unit_price REAL
        )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        sale_id TEXT PRIMARY KEY,
        product_id TEXT REFERENCES products(product_id),
        quantity INTEGER,
        sale_date TEXT,
        payment_method TEXT,
        customer_type TEXT
    )
    """)

    conn.commit()


def insert_products(conn: sqlite3.Connection, products_df) -> None:
    """
    Inserts every row of the cleaned products DataFrame into the products table.

    """

    rows = products_df[["product_id", "product_name", "category", "unit_price"]].itertuples(index=False, name=None)
    
    conn.executemany("""
        INSERT INTO products (
        product_id, product_name, category, unit_price
        )
        VALUES (?, ?, ?, ?)
        """,
        rows,
    )

    conn.commit()

def insert_sales(conn: sqlite3.Connection, sales_df) -> None:
    """
    Inserts every row of the cleaned sales DataFrame into the
    sales table.

    """

    missing = conn.execute("""
    SELECT DISTINCT s.product_id
        FROM sales AS s
        LEFT JOIN products AS p ON p.product_id = s.product_id
        WHERE p.product_id IS NULL
    """).fetchall()

    print(missing)

    columns = [
        "sale_id",
        "product_id",
        "quantity",
        "sale_date",
        "payment_method",
        "customer_type",
    ]

    rows = sales_df[columns].itertuples(index=False, name=None)

    conn.executemany("""
        INSERT INTO sales (
            sale_id, product_id, quantity, sale_date,
            payment_method, customer_type
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    conn.commit()

def query_total_revenue_per_product(conn: sqlite3.Connection):
    """
    Returns each product's name and its total revenue
    (quantity * unit_price, summed across all its sales), highest revenue first.
    """

    sql = """
        SELECT
            p.product_name,
            SUM(s.quantity * p.unit_price) AS total_revenue
        FROM sales AS s
        JOIN products AS p
            ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_revenue DESC
    """

    return conn.execute(sql).fetchall()

def query_best_selling_product(conn: sqlite3.Connection):
    """
    Returns a single product with the highest total quantity sold.
    """

    sql = """
        SELECT
            p.product_id,
            p.product_name,
            SUM(s.quantity) AS total_quantity_sold
        FROM sales AS s
        JOIN products AS p
            ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_quantity_sold DESC
        LIMIT 1
    """

    return conn.execute(sql).fetchone()

def query_sales_by_payment_method(conn: sqlite3.Connection):
    """
    Returns the number of sales transactions per payment_method.
    """

    sql = """
        SELECT
            payment_method,
            COUNT(*) AS transaction_count
        FROM sales
        GROUP BY payment_method
    """

    return conn.execute(sql).fetchall()


def query_custom_one(conn: sqlite3.Connection):
    """
    Returns the average quantity per transaction
    for each customer type.
    """

    sql = """
        SELECT
            customer_type,
            AVG(quantity) AS average_quantity_per_transaction
        FROM sales
        GROUP BY customer_type
    """

    return conn.execute(sql).fetchall()

def query_custom_two(conn: sqlite3.Connection):
    """
    Returns products that have sold more than 10 units in total.
    """

    sql = """
        SELECT
            p.product_name,
            SUM(s.quantity) AS total_quantity_sold
        FROM sales AS s
        JOIN products AS p
            ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        HAVING SUM(s.quantity) > 10
        ORDER BY total_quantity_sold DESC
    """

    return conn.execute(sql).fetchall()


def show_db_changes(conn: sqlite3.Connection, table: str) -> None:
    cursor = conn.execute(f"SELECT * FROM {table}")

    print(f"\n{table}")
    print([column[0] for column in cursor.description])

    for row in cursor.fetchall():
        print(row)

