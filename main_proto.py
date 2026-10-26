import os
import pandas as pd

import data_cleaning_proto as data_cleaning
import database_proto as database
import analysis_proto as analysis
import visualize_proto as visualize
import security_proto as security

DATA_DIR = "../data/"

PRODUCTS_CSV = DATA_DIR + "products.csv"
SALES_CSV = DATA_DIR + "sales.csv"
DB_PATH = DATA_DIR + "store.db"

def main():
    print("=" * 60)
    print("Thabo's Corner Store — Sales Insights System")
    print("=" * 60)

    # ---- Task 6: security gate -------------------------------------
    if not security.login_gate(security.STORED_PASSWORD_HASH):
        return

    # ---- Task 2: load & clean data ----------------------------------
    print("\n[1/5] Loading raw data...")
    raw_products, raw_sales = data_cleaning.load_raw_data(PRODUCTS_CSV, SALES_CSV)

    print("[2/5] Cleaning data...")
    clean_products = data_cleaning.clean_products(raw_products)
    valid_ids = clean_products["product_id"].tolist()
    clean_sales = data_cleaning.clean_sales(raw_sales, valid_product_ids=valid_ids)
    print(data_cleaning.cleaning_summary(raw_products, clean_products, "products"))
    print(data_cleaning.cleaning_summary(raw_sales, clean_sales, "sales"))

    # ---- Task 3: build the database ---------------------------------
    print("\n[3/5] Building database...")
    conn = database.get_connection(DB_PATH)
    database.create_tables(conn)
    database.insert_products(conn, clean_products)
    database.insert_sales(conn, clean_sales)

    print("\nSample SQL query results — revenue per product:")
    for row in database.query_total_revenue_per_product(conn):
        print("   ", row)

    # ---- Task 4: programming logic / analysis -----------------------
    print("\n[4/5] Running analysis...")
    sales_records = clean_sales.to_dict("records")
    products_records = clean_products.to_dict("records")

    print("Total sales records:", analysis.total_sales_records(sales_records))
    print("Low stock alerts:", analysis.low_stock_alert(products_records))
    trend = analysis.monthly_sales_trend(sales_records)
    print("Monthly trend:", trend)
    print("Average basket size:", analysis.average_basket_size(sales_records))

    # ---- Task 5: visualisation ---------------------------------------
    print("\n[5/5] Generating charts...")
    revenue_rows = database.query_total_revenue_per_product(conn)
    names = [r[0] for r in revenue_rows]
    revenues = [r[1] for r in revenue_rows]
    visualize.bar_chart_revenue_per_product(names, revenues)
    visualize.line_chart_monthly_trend(trend)
    print("Charts saved as revenue_per_product.png and monthly_trend.png")

    conn.close()
    print("\nDone! Don't forget to commit and push your progress to GitHub.")


if __name__ == "__main__":
    main()

