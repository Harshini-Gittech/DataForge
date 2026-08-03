"""
Module: Sales Data Generator
Purpose: Generate synthetic sales transactions from existing orders.
Author: Harshini
Project: DataForge
"""

import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

# ==========================
# Configuration
# ==========================

ORDER_FILE = Path("data/raw/orders/orders.csv")

OUTPUT_DIR = Path("data/raw/sales")
OUTPUT_FILE = OUTPUT_DIR / "sales.csv"

TAX_RATE = 0.18

# Discount percentages
DISCOUNT_PERCENTAGES = [0, 5, 10, 15]

# Business Rules:
# Sales Channel -> Allowed Payment Methods
SALES_CHANNELS = {
    "Online": [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
    ],
    "Mobile App": [
        "UPI",
        "Credit Card",
        "Debit Card",
    ],
    "Store": [
        "Cash",
        "UPI",
        "Credit Card",
        "Debit Card",
    ],
}

# City -> Region Mapping
CITY_REGION = {
    "Bengaluru": "South",
    "Chennai": "South",
    "Hyderabad": "South",
    "Kochi": "South",

    "Mumbai": "West",
    "Pune": "West",
    "Ahmedabad": "West",

    "Delhi": "North",
    "Jaipur": "North",
    "Lucknow": "North",

    "Kolkata": "East",
    "Bhubaneswar": "East",
    "Guwahati": "East",
}


def generate_sales() -> None:
    """
    Generate sales transactions using existing order data.
    """

    orders = pd.read_csv(ORDER_FILE)

    sales = []

    for index, order in orders.iterrows():

        order_id = order["order_id"]
        customer_id = order["customer_id"]
        product_id = order["product_id"]

        quantity = int(order["quantity"])
        unit_price = round(float(order["unit_price"]), 2)

        # Financial calculations
        subtotal = quantity * unit_price

        discount_percent = random.choice(DISCOUNT_PERCENTAGES)

        discount = round(
            subtotal * discount_percent / 100,
            2
        )

        tax = round(subtotal * TAX_RATE, 2)

        total_amount = round(
            subtotal - discount + tax,
            2
        )

        # Business Rule:
        # Cash only available for Store
        sales_channel = random.choice(
            list(SALES_CHANNELS.keys())
        )

        payment_method = random.choice(
            SALES_CHANNELS[sales_channel]
        )

        # Region derived from city
        city = random.choice(
            list(CITY_REGION.keys())
        )

        region = CITY_REGION[city]

        # Random sale date within last year
        sale_date = fake.date_between(
            start_date="-1y",
            end_date="today"
        )

        sales.append(
            {
                "sale_id": f"SALE{index + 1:06}",
                "order_id": order_id,
                "customer_id": customer_id,
                "product_id": product_id,
                "sale_date": sale_date,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount,
                "tax": tax,
                "total_amount": total_amount,
                "payment_method": payment_method,
                "city": city,
                "region": region,
                "sales_channel": sales_channel,
            }
        )

    df = pd.DataFrame(sales)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 50)
    print(f"Generated {len(df)} sales transactions")
    print(f"Saved to: {OUTPUT_FILE}")
    print("=" * 50)


def main() -> None:
    """
    Entry point of the program.
    """
    generate_sales()


if __name__ == "__main__":
    main()