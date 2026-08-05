"""
Module: ETL Pipeline
Purpose: Extract, Transform and Load cleaned datasets.
Author: Harshini
Project: DataForge
"""

from pathlib import Path
import pandas as pd

# ==========================
# Raw Files
# ==========================

CUSTOMERS_FILE = Path("data/raw/customers/customers.csv")
PRODUCTS_FILE = Path("data/raw/products/products.csv")
ORDERS_FILE = Path("data/raw/orders/orders.csv")
SALES_FILE = Path("data/raw/sales/sales.csv")

# ==========================
# Output Files
# ==========================

CUSTOMERS_OUTPUT = Path(
    "data/processed/customers/customers_clean.csv"
)

PRODUCTS_OUTPUT = Path(
    "data/processed/products/products_clean.csv"
)

ORDERS_OUTPUT = Path(
    "data/processed/orders/orders_clean.csv"
)

SALES_OUTPUT = Path(
    "data/processed/sales/sales_clean.csv"
)


def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV file.
    """
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save DataFrame to CSV.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(output_path, index=False)


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean customer dataset.
    """

    df = df.drop_duplicates(
        subset="customer_id"
    )

    df = df.dropna(
        how="all"
    )

    return df


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean product dataset.
    """

    df = df.drop_duplicates(
        subset="product_id"
    )

    df = df[df["price"] >= 0]

    df = df[df["stock_quantity"] >= 0]

    return df


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean orders dataset.
    """

    df = df.drop_duplicates(
        subset="order_id"
    )

    df = df[df["quantity"] > 0]

    return df


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sales dataset.
    """

    df = df.drop_duplicates(
        subset="sale_id"
    )

    # Remove rows where total_amount is negative
    df = df[df["total_amount"] >= 0]

    return df


def process_dataset(
    name: str,
    input_file: Path,
    output_file: Path,
    cleaning_function,
) -> None:
    """
    Generic ETL process.
    """

    print(f"\nLoading {name}...")

    df = load_csv(input_file)

    print(f"{len(df)} records loaded")

    cleaned_df = cleaning_function(df)

    save_csv(cleaned_df, output_file)

    print(f"{len(cleaned_df)} records saved")


def main() -> None:
    """
    Execute the ETL pipeline.
    """

    print("=" * 40)
    print("ETL PIPELINE STARTED")
    print("=" * 40)

    process_dataset(
        "Customers",
        CUSTOMERS_FILE,
        CUSTOMERS_OUTPUT,
        clean_customers,
    )

    process_dataset(
        "Products",
        PRODUCTS_FILE,
        PRODUCTS_OUTPUT,
        clean_products,
    )

    process_dataset(
        "Orders",
        ORDERS_FILE,
        ORDERS_OUTPUT,
        clean_orders,
    )

    process_dataset(
        "Sales",
        SALES_FILE,
        SALES_OUTPUT,
        clean_sales,
    )

    print("\n" + "=" * 40)
    print("ETL COMPLETED SUCCESSFULLY")
    print("=" * 40)


if __name__ == "__main__":
    main()