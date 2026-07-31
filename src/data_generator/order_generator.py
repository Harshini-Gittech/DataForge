"""
Module: Order Data Generator
Purpose: Generate synthetic order data using existing customers and products.
Author: Harshini
Project: DataForge
"""

import random
from pathlib import Path

import pandas as pd

# ==========================
# Configuration
# ==========================

NUM_ORDERS = 100

CUSTOMER_FILE = Path("data/raw/customers/customers.csv")
PRODUCT_FILE = Path("data/raw/products/products.csv")
OUTPUT_DIR = Path("data/raw/orders")
OUTPUT_FILE = OUTPUT_DIR / "orders.csv"

PAYMENT_STATUS = [
    "Paid",
    "Pending",
    "Failed",
    "Refunded"
]

ORDER_STATUS = [
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled"
]


def generate_orders(num_orders: int = NUM_ORDERS) -> None:
    """
    Generate synthetic order data using customer
    and product datasets.
    """

    customers = pd.read_csv(CUSTOMER_FILE)
    products = pd.read_csv(PRODUCT_FILE)

    orders = []

    for i in range(1, num_orders + 1):

        customer = customers.sample(n=1).iloc[0]
        product = products.sample(n=1).iloc[0]

        quantity = random.randint(1, 5)
        unit_price = round(float(product["price"]), 2)
        total_amount = round(quantity * unit_price, 2)

        orders.append(
            {
                "order_id": f"ORD{i:06}",
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total_amount,
                "order_date": pd.Timestamp.today().date(),
                "payment_status": random.choice(PAYMENT_STATUS),
                "order_status": random.choice(ORDER_STATUS),
            }
        )

    df = pd.DataFrame(orders)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 45)
    print(f"Generated {len(df)} orders")
    print(f"Saved to: {OUTPUT_FILE}")
    print("=" * 45)


def main() -> None:
    """
    Entry point of the program.
    """
    generate_orders()


if __name__ == "__main__":
    main()