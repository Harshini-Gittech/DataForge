"""
Module: Data Quality Validation
Purpose: Validate generated datasets.
Author: Harshini
Project: DataForge
"""

from pathlib import Path
import pandas as pd

# ==========================
# File Paths
# ==========================

CUSTOMERS_FILE = Path("data/raw/customers/customers.csv")
PRODUCTS_FILE = Path("data/raw/products/products.csv")
ORDERS_FILE = Path("data/raw/orders/orders.csv")
SALES_FILE = Path("data/raw/sales/sales.csv")

def load_data():
    customers = pd.read_csv(CUSTOMERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    orders = pd.read_csv(ORDERS_FILE)
    sales = pd.read_csv(SALES_FILE)

    return customers, products, orders, sales


def check_unique_ids(df, column_name):
    return df[column_name].is_unique

def check_positive_values(df, column_name):
    return (df[column_name] > 0).all()

def check_non_negative(df, column_name):
    return (df[column_name] >= 0).all()

def check_foreign_keys(child_df, parent_df, child_column, parent_column):
    return child_df[child_column].isin(parent_df[parent_column]).all()

def check_order_amount(df):
    expected = (df["quantity"] * df["unit_price"]).round(2)
    actual = df["total_amount"].round(2)

    return expected.equals(actual)

def check_sales_amount(df):
    return (df["total_amount"] >= 0).all()

def main():

    customers, products, orders, sales = load_data()

    print("=" * 40)
    print("DATA QUALITY REPORT")
    print("=" * 40)

    print("\nCustomers")
    customer_unique = check_unique_ids(customers, "customer_id")
    print(f"{'PASS' if customer_unique else 'FAIL'} - Unique Customer IDs")

    print("\nProducts")
    product_unique = check_unique_ids(products, "product_id")
    print(f"{'PASS' if product_unique else 'FAIL'} - Unique Product IDs")

    price_check = check_positive_values(products, "price")
    print(f"{'PASS' if price_check else 'FAIL'} - Positive Prices")

    stock_check = check_non_negative(products, "stock_quantity")
    print(f"{'PASS' if stock_check else 'FAIL'} - Non-negative Stock")

    print("\nOrders")
    order_customer_fk = check_foreign_keys(
        orders,
        customers,
        "customer_id",
        "customer_id"
    )
    print(f"{'PASS' if order_customer_fk else 'FAIL'} - Customer Foreign Keys")

    order_product_fk = check_foreign_keys(
        orders,
        products,
        "product_id",
        "product_id"
    )
    print(f"{'PASS' if order_product_fk else 'FAIL'} - Product Foreign Keys")

    order_amount = check_order_amount(orders)
    print(f"{'PASS' if order_amount else 'FAIL'} - Amount Validation")

    print("\nSales")
    sales_order_fk = check_foreign_keys(
        sales,
        orders,
        "order_id",
        "order_id"
    )
    print(f"{'PASS' if sales_order_fk else 'FAIL'} - Order Foreign Keys")

    sales_customer_fk = check_foreign_keys(
        sales,
        customers,
        "customer_id",
        "customer_id"
    )
    print(f"{'PASS' if sales_customer_fk else 'FAIL'} - Customer Foreign Keys")

    sales_product_fk = check_foreign_keys(
        sales,
        products,
        "product_id",
        "product_id"
    )
    print(f"{'PASS' if sales_product_fk else 'FAIL'} - Product Foreign Keys")

    sales_amount = check_sales_amount(sales)
    print(f"{'PASS' if sales_amount else 'FAIL'} - Non-negative Amount")

    all_checks = (
        customer_unique
        and product_unique
        and price_check
        and stock_check
        and order_customer_fk
        and order_product_fk
        and order_amount
        and sales_order_fk
        and sales_customer_fk
        and sales_product_fk
        and sales_amount
    )

    print("\n" + "=" * 40)

    if all_checks:
        print("OVERALL STATUS: ALL CHECKS PASSED")
    else:
        print("OVERALL STATUS: SOME CHECKS FAILED")

    print("=" * 40)

if __name__ == "__main__":
    main()    