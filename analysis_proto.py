import data_cleaning_proto as data_helpers

def total_sales_records(sales_rows: list) -> int:
    """
    """

    total = 0

    for row in sales_rows:
        total += 1

    return total

def low_stock_alert(products_rows: list, threshold: int = 5) -> list:

    """
    """
    
    out_of_stock = []

    for product in products_rows:
        if not product["in_stock"]:
            out_of_stock.append(product["product_name"])

    return out_of_stock


def monthly_sales_trend(sales_rows: list) -> dict:
    monthly_sales_per_product = {}
    
    for sale in sales_rows:
        month = sale["sale_date"][:7] 
        monthly_sales_per_product[month] = monthly_sales_per_product.get(month, 0) + sale["quantity"]


    return monthly_sales_per_product


def classify_transaction_size(quantity: int) -> str:
    """
    """

    if quantity >= 5:
        return "Bulk"
    elif quantity >= 2:
        return "Multiple"
    elif quantity == 1:
        return "Single"
    else:
        return "Invalid"


def average_basket_size(sales_rows: list) -> float:
    """
    """

    total = 0
    for sale in sales_rows:
        total += sale["quantity"]

    avg = total / len(sales_rows)

    return round(avg, 2)

ROOT_DIR = "../data/"
PRODUCTS_CSV = ROOT_DIR + "products.csv"
SALES_CSV = ROOT_DIR + "sales.csv"

(products_df, sales_df) = data_helpers.load_raw_data(PRODUCTS_CSV, SALES_CSV)

valid_product_ids = products_df["product_id"].astype(str).str.strip().tolist()

products_df = data_helpers.clean_products(products_df)
sales_df = data_helpers.clean_sales(sales_df, valid_product_ids)
print(sales_df)
products = products_df.to_dict(orient="records")
sales = sales_df.to_dict(orient="records")

print("[+] Total sales records: " + str(total_sales_records(sales)))
print("[-] Low stock products: ") 
print(low_stock_alert(products))

print("[+] Monthly sales trend: ") 
print(monthly_sales_trend(sales))
print("[+] Transaction sizes 5: " + classify_transaction_size(5))
print("[+] Transaction sizes 3: " + classify_transaction_size(3))
print("[+] Transaction sizes 1: " + classify_transaction_size(1))
print("[+] Average basket size: " + str(average_basket_size(sales)))
