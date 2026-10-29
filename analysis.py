def total_sales_records(sales_rows: list) -> int:
    """
    Counts how many sales records there are, using a loop.
    Args:
        sales_rows: a list of dictionaries, one per sale, e.g.
            [{"product_id": "P001", "quantity": 2, ...}, ...]

    Returns:
        the total number of records, as an integer, counted with a loop.

    """

    total = 0

    for row in sales_rows:
        total += 1

    return total

def low_stock_alert(products_rows: list, threshold: int = 5) -> list:

    """
    Builds a list of product names where in_stock is False.

    Args:
        products_rows: list of dictionaries, one per product
        threshold: (optional) use this if you extend the dataset with
            a stock-count column later

    Returns:
        a list of product_name strings that need re-ordering.
    """
    
    out_of_stock = []

    for product in products_rows:
        if not product["in_stock"]:
            out_of_stock.append(product["product_name"])

    return out_of_stock


def monthly_sales_trend(sales_rows: list) -> dict:
    """
    Builds a dictionary that maps each month (e.g. "2026-01") to the total quantity sold that month, using a loop.

    Args:
        sales_rows: list of dictionaries, one per sale, each with a
            "sale_date" key already cleaned to "YYYY-MM-DD" format
            and a "quantity" key (as an int)

    Returns:
        a dict like {"2026-01": 143, "2026-02": 97}
    """

    monthly_sales_per_product = {}
    
    for sale in sales_rows:
        month = sale["sale_date"][:7] 
        monthly_sales_per_product[month] = monthly_sales_per_product.get(month, 0) + sale["quantity"]


    return monthly_sales_per_product


def classify_transaction_size(quantity: int) -> str:
    """
    Classifies transaction sizes with the rules:
        quantity >= 5   -> "Bulk"
        quantity >= 2   -> "Multiple"
        quantity == 1   -> "Single"
        anything else   -> "Invalid"

    Args:
        quantity: The transaction size to be classified.

    Returns:
        A class the quantity belongs to e.g. "Bulk", "Single"...

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
    Calculates the average quantity per sale across ALL sales, using a loop.
    
    Args:
        sales_rows: Sales records 

    Returns:
        a float rounded to 2 decimal places.

    """

    total = 0
    for sale in sales_rows:
        total += sale["quantity"]

    avg = total / len(sales_rows)

    return round(avg, 2)
