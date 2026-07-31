"""
Module: Order Data Generator
Purpose: Generate synthetic order data using existing customers and products.
Author: Harshini
Project: DataForge
"""

import random
from pathlib import Path

import pandas as pd

NUM_ORDERS = 100

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


def generate_orders(num_orders=NUM_ORDERS):
    """
    Generate synthetic order data using customer and product datasets.
    """

    customers = pd.read_csv("data/raw/customers/customers.csv")
    products = pd.read_csv("data/raw/products/products.csv")

    orders = []

    for i in range(1, num_orders + 1):

        customer = customers.sample(1).iloc[0]
        product = products.sample(1).iloc[0]

        quantity = random.randint(1, 5)
        unit_price = float(product["price"])
        total_amount = round(quantity * unit_price, 2)

        orders.append({
            "order_id": f"ORD{i:06}",
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount,
            "order_date": pd.Timestamp.today().date(),
            "payment_status": random.choice(PAYMENT_STATUS),
            "order_status": random.choice(ORDER_STATUS)
        })

    df = pd.DataFrame(orders)

    output_dir = Path("data/raw/orders")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "orders.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} orders.")
    print(f"Saved to {output_file}")


def main():
    generate_orders()


if __name__ == "__main__":
    main()