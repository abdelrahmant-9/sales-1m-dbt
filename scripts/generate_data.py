"""Create 1,200,000 fake sales rows (plus customers, products, stores) and load them into DuckDB.

Step 1: write CSV files into data/raw/
Step 2: load every CSV into the `raw` schema of warehouse/sales.duckdb

Run: uv run python scripts/generate_data.py
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

import duckdb

random.seed(42)
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

N_SALES = 1_200_000
CITIES = ["Cairo", "Alexandria", "Giza", "Riyadh", "Jeddah", "Dubai", "Abu Dhabi", "Doha", "Kuwait City", "Amman"]
CATEGORIES = ["Electronics", "Home", "Grocery", "Fashion", "Beauty", "Sports", "Toys", "Books"]
CHANNELS = ["online", "mall", "street"]


def write_csv(name, header, rows):
    with open(RAW / f"{name}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


# customers
customers = [
    (i, f"Customer {i}", random.choice(CITIES), random.choice(["M", "F"]))
    for i in range(1, 50_001)
]
write_csv("customers", ["customer_id", "customer_name", "city", "gender"], customers)

# products
products = [
    (i, f"SKU-{i:05d}", random.choice(CATEGORIES), round(random.uniform(5, 1000), 2))
    for i in range(1, 501)
]
write_csv("products", ["product_id", "sku", "category", "list_price"], products)

# stores
stores = [(i, f"Store #{i}", random.choice(CHANNELS)) for i in range(1, 41)]
write_csv("stores", ["store_id", "store_name", "channel"], stores)

# sales (2 years of transactions)
start = datetime(2024, 1, 1)
seconds_in_2_years = 2 * 365 * 24 * 60 * 60
with open(RAW / "sales.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id", "sold_at", "customer_id", "product_id", "store_id", "quantity", "discount_pct"])
    for i in range(1, N_SALES + 1):
        writer.writerow([
            i,
            (start + timedelta(seconds=random.randint(0, seconds_in_2_years))).strftime("%Y-%m-%d %H:%M:%S"),
            random.randint(1, 50_000),
            random.randint(1, 500),
            random.randint(1, 40),
            random.randint(1, 5),
            random.choice([0, 0, 0, 0.05, 0.10, 0.20]),
        ])
print("CSV files created in data/raw/")

# load into DuckDB
con = duckdb.connect(str(ROOT / "warehouse" / "sales.duckdb"))
con.execute("create schema if not exists raw")
for name in ["customers", "products", "stores", "sales"]:
    con.execute(f"create or replace table raw.{name} as select * from read_csv('{RAW / name}.csv')")
    count = con.execute(f"select count(*) from raw.{name}").fetchone()[0]
    print(f"raw.{name}: {count:,} rows")
