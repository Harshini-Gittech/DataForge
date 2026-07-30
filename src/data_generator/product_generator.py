"""
Module: Product Data Generator
Purpose: Generate synthetic product catalog for DataForge
Author: Harshini
Project: DataForge
"""

import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

NUM_PRODUCTS = 100

CATEGORIES = {
    "Electronics": ["Logitech", "Samsung", "Sony", "HP"],
    "Home & Kitchen": ["Prestige", "Pigeon", "Philips"],
    "Fashion": ["Nike", "Adidas", "Puma"],
    "Books": ["Penguin", "HarperCollins", "O'Reilly"],
    "Beauty": ["Lakme", "Nivea", "L'Oréal"]
}


def generate_products(num_products=NUM_PRODUCTS):
    """
    Generate synthetic product data and save it as a CSV file.
    """

    products = []

    for i in range(1, num_products + 1):

        category = random.choice(list(CATEGORIES.keys()))
        brand = random.choice(CATEGORIES[category])

        products.append({
            "product_id": f"PROD{i:06}",
            "product_name": fake.word().title(),
            "category": category,
            "brand": brand,
            "price": round(random.uniform(99, 5000), 2),
            "stock_quantity": random.randint(10, 500),
            "supplier": fake.company(),
            "created_date": fake.date_this_year()
        })

    df = pd.DataFrame(products)

    output_dir = Path("data/raw/products")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "products.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} products.")
    print(f"Saved to {output_file}")


def main():
    generate_products()


if __name__ == "__main__":
    main()