"""
Module: Customer Data Generator
Purpose: Generate synthetic customer data for DataForge
Author: Harshini
Project: DataForge
"""

import pandas as pd
from faker import Faker
import random
from pathlib import Path

fake = Faker("en_IN")


def generate_customers(num_records=10):
    """
    Generate synthetic customer data.
    """

    customers = []

    for i in range(1, num_records + 1):
        customers.append({
            "customer_id": f"CUST{i:06}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "gender": random.choice(["Male", "Female"]),
            "date_of_birth": fake.date_of_birth(
                minimum_age=18,
                maximum_age=60
            ),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "city": fake.city(),
            "state": "Karnataka",
            "country": "India",
            "registration_date": fake.date_this_year(),
            "status": random.choice(["Active", "Inactive"])
        })

    df = pd.DataFrame(customers)

    output_dir = Path("data/raw/customers")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "customers.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} customer records.")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_customers(10)