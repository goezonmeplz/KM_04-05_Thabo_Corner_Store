import matplotlib.pyplot as plt
import data_cleaning_proto as data_helpers
import random
import analysis_proto as analysis_helpers
def bar_chart_revenue_per_product(product_names: list, revenues: list, save_path: str = "revenue_per_product.png"):
    """
    """

    plt.figure(figsize=(10, 6))
    plt.bar(product_names, revenues)
    plt.xticks(rotation = 45, ha = "right")
    plt.ylabel("Revenue (R)")
    plt.title("""Total Revenue per Product - Thabo's
        Corner Store
    """)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def line_chart_monthly_trend(monthly_trend: dict, save_path: str = "monthly_trend.png"):
    """
    """

    months = list(monthly_trend.keys())
    totals = list(monthly_trend.values())
    plt.figure(figsize=(8, 5))
    plt.plot(months, totals, marker = "o")
    plt.ylabel("Units Sold")
    plt.title("Monthly Sales Trend - Thabo's Corner Store")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

ROOT_DIR = "../data/"
PRODUCTS_CSV = ROOT_DIR + "products.csv"
SALES_CSV = ROOT_DIR + "sales.csv"

(products_df, sales_df) = data_helpers.load_raw_data(PRODUCTS_CSV, SALES_CSV)

valid_product_ids = products_df["product_id"].astype(str).str.strip().tolist()

products_df = data_helpers.clean_products(products_df)
sales_df = data_helpers.clean_sales(sales_df, valid_product_ids)

# Use
products = products_df.to_dict(orient="records")
sales = sales_df.to_dict(orient="records")

product_names = list({row["product_name"] for row in products})
revenues = [random.randint(0, 100) for _ in range(len(product_names))]


bar_chart_revenue_per_product(product_names, revenues)
line_chart_monthly_trend(analysis_helpers.monthly_sales_trend(sales))
