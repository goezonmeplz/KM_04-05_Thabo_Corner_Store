import pandas as pd

def load_raw_data(products_path: str, sales_path: str):
    """
    """

    products_df = pd.read_csv(products_path)
    sales_df = pd.read_csv(sales_path)

    return (products_df, sales_df)

def clean_products(products_df: "pd.DataFrame") -> "pd.DataFrame":

    """
    """

    products_df = products_df.copy()
    
    # Remove rows with: empty unit_price and product_name fields
    products_df = products_df.dropna(subset=["unit_price"])
    products_df = products_df.dropna(subset=["product_name"])

    # Make capitalization consistent
    products_df["category"] = products_df["category"].str.capitalize()
    
    # Remove duplicate rows
    products_df = products_df.drop_duplicates()

    return products_df


def clean_sales(sales_df: "pd.DataFrame", valid_product_ids) -> "pd.DataFrame":
    """
    """

    sales_df = sales_df.copy()

    print(sales_df)

    # Format dates as YYYY-MM-DD
    sales_df["parsed_date"] = pd.to_datetime(pd.NA, errors='coerce')

    formats = ["%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]

    for fmt in formats:
        # Find rows where we haven't successfully parsed the date yet
        missing = sales_df["parsed_date"].isna()
    
        # Try parsing the ORIGINAL string column using the current format
        parsed = pd.to_datetime(sales_df.loc[missing, "sale_date"], format=fmt, errors='coerce')
    
        # Save the successful parses into the temporary column
        sales_df.loc[missing, "parsed_date"] = parsed

    # Now replace the original string column with the successfully parsed dates
    sales_df["sale_date"] = sales_df["parsed_date"]
    sales_df = sales_df.drop(columns=["parsed_date"])
    sales_df["sale_date"] = sales_df["sale_date"].dt.strftime('%Y-%m-%d')

    # If the above parsing fails, then the date was empty, remove the row
    sales_df = sales_df.dropna(subset=["sale_date"])

    # Only keep rows with a valid product_id
    sales_df = sales_df[sales_df["product_id"].isin(valid_product_ids)]
   
    # Remove rows with a missing quantity
    sales_df = sales_df.dropna(subset=["quantity"])

    # Rows with a missing payment_method get assigned Unknown
    sales_df["payment_method"] = sales_df["payment_method"].fillna("Unknown")
    
    # Remove duplicate rows
    sales_df = sales_df.drop_duplicates()

    # Rows with an empty customer_type get assigned Unknown
    sales_df["customer_type"] = sales_df["customer_type"].fillna("Unknown")

    return sales_df

def cleaning_summary(raw_df: "pd.DataFrame", clean_df: "pd.DataFrame", name: str) -> str:
    """
    """
    
    raw_count = len(raw_df)
    clean_count = len(clean_df)
    removed = raw_count - clean_count

    return f"{name}: {raw_count} raw rows -> {clean_count} clean rows ({removed} removed)"

    
ROOT_DIR = "../data/"
PRODUCTS = ROOT_DIR + "products.csv"
SALES = ROOT_DIR + "sales.csv"

(products_df, sales_df) = load_raw_data(PRODUCTS, SALES)
#cleaned_products = clean_products(products_df)
#print(cleaned_products)

valid_product_ids = ['P' + f"{i:03}" for i in range(0, 1000)]
print(valid_product_ids)
cleaned_sales = clean_sales(sales_df, valid_product_ids)
print(cleaned_sales)
print(cleaning_summary(sales_df, cleaned_sales, "sales"))
