import csv
import psycopg2
from pathlib import Path

# --- Database connection settings ---
# Matches the credentials defined in docker-compose.yml
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

# --- Path to the source CSV file ---
# Path(__file__) resolves relative to this script's location, not the working directory
CSV_PATH = Path(__file__).parent / "data" / "campus_bites_orders.csv"

# --- Table definition ---
# IF NOT EXISTS makes this safe to run multiple times without error
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id            INTEGER PRIMARY KEY,
    order_date          DATE,
    order_time          TIME,
    customer_segment    TEXT,
    order_value         NUMERIC(10, 2),
    cuisine_type        TEXT,
    delivery_time_mins  INTEGER,
    promo_code_used     BOOLEAN,
    is_reorder          BOOLEAN
);
"""

# --- Insert statement ---
# ON CONFLICT DO NOTHING skips duplicate order_ids, making the script idempotent
INSERT_ROW = """
INSERT INTO orders (
    order_id, order_date, order_time, customer_segment, order_value,
    cuisine_type, delivery_time_mins, promo_code_used, is_reorder
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (order_id) DO NOTHING;
"""


def parse_bool(value):
    # Converts "Yes"/"No" strings from the CSV into Python booleans
    return value.strip().lower() == "yes"


def load_data():
    # Open a connection to the PostgreSQL database
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn:  # Acts as a transaction — commits on success, rolls back on error
            with conn.cursor() as cur:
                # Create the orders table if it doesn't already exist
                cur.execute(CREATE_TABLE)

                # Read and parse every row from the CSV into a list of tuples
                with open(CSV_PATH, newline="") as f:
                    reader = csv.DictReader(f)
                    rows = [
                        (
                            int(row["order_id"]),
                            row["order_date"],
                            row["order_time"],
                            row["customer_segment"],
                            float(row["order_value"]),
                            row["cuisine_type"],
                            int(row["delivery_time_mins"]),
                            parse_bool(row["promo_code_used"]),
                            parse_bool(row["is_reorder"]),
                        )
                        for row in reader
                    ]

                # Insert all rows in a single batched call
                cur.executemany(INSERT_ROW, rows)
                print(f"Loaded {len(rows)} rows into orders.")
    finally:
        conn.close()


if __name__ == "__main__":
    load_data()
