import sqlite3
import data_cleaning_proto

ROOT_DIR = "../data/"

PRODUCTS_CSV = ROOT_DIR + "products.csv"
SALES_CSV = ROOT_DIR + "sales.csv"

STORE_DB = ROOT_DIR + "store.db"

def get_connection(db_path: str = STORE_DB) -> sqlite3.Connection:
    """
    """

    conn = sqlite3.connect(STORE_DB)
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    """
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
    What is the average quantity per transaction
    for each customer type?
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
    Which products have sold more than 10 units in total?
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

conn = get_connection()
(products_df, sales_df) = data_cleaning_proto.load_raw_data(PRODUCTS_CSV, SALES_CSV)
products_df = data_cleaning_proto.clean_products(products_df)

valid_product_ids = products_df["product_id"].astype(str).str.strip().tolist()
sales_df = data_cleaning_proto.clean_sales(sales_df, valid_product_ids)

create_tables(conn)

print("[+] INSERTING PRODUCTS")
insert_products(conn, products_df)
show_db_changes(conn, "products")

print("[+] INSERTING SALES")
insert_sales(conn, sales_df)
show_db_changes(conn, "sales")

print(query_total_revenue_per_product(conn))
print(query_best_selling_product(conn))
print(query_sales_by_payment_method(conn))
print(query_custom_one(conn))
print(query_custom_two(conn))
