"""
Data Loader and Feature Engineering Module for Afficionado Coffee Roasters.
Reads the original Excel dataset in read-only mode, performs feature engineering,
and exports the processed dataset separately to outputs/cleaned_transactions.csv.
"""

import os
import datetime
import pandas as pd
import numpy as np

RAW_EXCEL_PATH = "Afficionado Coffee Roasters.xlsx"
PROCESSED_CSV_PATH = os.path.join("outputs", "cleaned_transactions.csv")


def extract_hour(t):
    """Safely extracts integer hour (0-23) from Excel time object, float, or string."""
    if isinstance(t, datetime.time):
        return t.hour
    elif isinstance(t, str):
        # Format "HH:MM:SS" or similar
        return int(t.split(":")[0])
    elif isinstance(t, (int, float)):
        # Excel fraction of day: 0.0 to 1.0
        return int(t * 24)
    return -1


def assign_daypart_unified_mentor(hour):
    """
    Unified Mentor Prescribed Time Buckets:
    - Morning: 06:00 - 11:59
    - Afternoon: 12:00 - 16:59
    - Evening: 17:00 - 21:59
    - Late Hours: 22:00 - 05:59
    """
    if 6 <= hour <= 11:
        return "Morning (06:00-11:59)"
    elif 12 <= hour <= 16:
        return "Afternoon (12:00-16:59)"
    elif 17 <= hour <= 21:
        return "Evening (17:00-21:59)"
    else:
        return "Late Hours (22:00-05:59)"


def assign_demand_tier(hour):
    """
    Empirical Demand Tier Classification based on actual transaction counts:
    - Peak (>10,000 transactions/hr): Hours 07, 08, 09, 10
    - Moderate (7,000 - 10,000 transactions/hr): Hours 11, 12, 13, 14, 15, 16, 17, 18
    - Off-Peak (<7,000 transactions/hr): Hours 06, 19, 20
    """
    if hour in [7, 8, 9, 10]:
        return "Peak"
    elif hour in [11, 12, 13, 14, 15, 16, 17, 18]:
        return "Moderate"
    elif hour in [6, 19, 20]:
        return "Off-Peak"
    else:
        return "Closed"


def load_and_process_data(raw_path=RAW_EXCEL_PATH, save_csv=True):
    """
    Loads raw Excel dataset, validates structure, performs feature engineering,
    and returns processed DataFrame.
    """
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Original Excel dataset not found at {raw_path}")

    print(f"Loading raw dataset from '{raw_path}' (read-only)...")
    df = pd.read_excel(raw_path, sheet_name="Transactions")

    # Validation
    expected_rows = 149116
    actual_rows = len(df)
    print(f"Total records loaded: {actual_rows:,}")
    if actual_rows != expected_rows:
        print(f"Warning: Expected {expected_rows:,} rows, but found {actual_rows:,}")

    # Validate duplicate IDs
    duplicate_count = df["transaction_id"].duplicated().sum()
    if duplicate_count > 0:
        raise ValueError(f"Found {duplicate_count} duplicate transaction IDs!")
    print("Integrity check passed: 0 duplicate transaction IDs.")

    # Feature Engineering
    # 1. Calculated Gross Revenue
    df["revenue"] = (df["unit_price"] * df["transaction_qty"]).round(2)

    # 2. Integer Hour extraction
    df["hour"] = df["transaction_time"].apply(extract_hour)

    # 3. Formatted Hour Label (e.g. "08:00 - 08:59")
    df["hour_label"] = df["hour"].apply(lambda h: f"{h:02d}:00 - {h:02d}:59")

    # 4. Daypart (Unified Mentor exact buckets)
    df["daypart"] = df["hour"].apply(assign_daypart_unified_mentor)

    # 5. Demand Tier (Peak, Moderate, Off-Peak)
    df["demand_tier"] = df["hour"].apply(assign_demand_tier)

    # Check for nulls in new columns
    null_counts = df.isnull().sum()
    print("Null check summary:\n", null_counts[null_counts > 0])

    if save_csv:
        os.makedirs(os.path.dirname(PROCESSED_CSV_PATH), exist_ok=True)
        print(f"Saving processed dataset to '{PROCESSED_CSV_PATH}'...")
        df.to_csv(PROCESSED_CSV_PATH, index=False)
        print(f"Processed dataset successfully saved. File size: {os.path.getsize(PROCESSED_CSV_PATH):,} bytes.")

    return df


def get_data():
    """Convenience function to load processed data from CSV if exists, else process from Excel."""
    if os.path.exists(PROCESSED_CSV_PATH):
        return pd.read_csv(PROCESSED_CSV_PATH)
    else:
        return load_and_process_data(save_csv=True)


if __name__ == "__main__":
    df_processed = load_and_process_data()
    print("\nProcessed Data Sample (first 3 rows):")
    cols_to_show = ["transaction_id", "year", "hour", "hour_label", "daypart", "demand_tier", "store_location", "product_category", "unit_price", "transaction_qty", "revenue"]
    print(df_processed[cols_to_show].head(3).to_string(index=False))
