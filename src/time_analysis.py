"""
Time Analysis Module for Afficionado Coffee Roasters.
Performs hourly sales analysis, Unified Mentor dayparts segmentation,
peak/moderate/off-peak classification, and store-specific hourly matrix.
"""

import os
import pandas as pd
import numpy as np

OUTPUT_DIR = "outputs"


def run_time_analysis():
    data_path = os.path.join(OUTPUT_DIR, "cleaned_transactions.csv")
    if not os.path.exists(data_path):
        from data_loader import get_data
        df = get_data()
    else:
        df = pd.read_csv(data_path)

    total_trans = len(df)
    total_rev = df["revenue"].sum()
    total_units = df["transaction_qty"].sum()

    print("=" * 60)
    print("MODULE 2: HOURLY PERFORMANCE (06:00 TO 20:00)")
    print("=" * 60)

    hourly = df.groupby(["hour", "hour_label", "demand_tier"]).agg(
        transactions=("transaction_id", "count"),
        units_sold=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum"),
        atv=("revenue", "mean")
    ).reset_index().sort_values(by="hour").reset_index(drop=True)

    hourly["pct_transactions"] = (hourly["transactions"] / total_trans) * 100
    hourly["pct_units"] = (hourly["units_sold"] / total_units) * 100
    hourly["pct_revenue"] = (hourly["total_revenue"] / total_rev) * 100

    print(hourly.to_string(index=False, columns=[
        "hour", "hour_label", "demand_tier", "transactions", "pct_transactions", "units_sold", "total_revenue", "pct_revenue", "atv"
    ], formatters={
        "transactions": "{:,}".format,
        "units_sold": "{:,}".format,
        "total_revenue": "${:,.2f}".format,
        "atv": "${:.2f}".format,
        "pct_transactions": "{:.2f}%".format,
        "pct_revenue": "{:.2f}%".format
    }))

    hourly_csv_path = os.path.join(OUTPUT_DIR, "02_hourly_performance.csv")
    hourly.to_csv(hourly_csv_path, index=False)
    print(f"Saved: {hourly_csv_path}")

    # Module 3: Unified Mentor Dayparts
    print("\n" + "=" * 60)
    print("MODULE 3: UNIFIED MENTOR DAYPARTS PERFORMANCE")
    print("=" * 60)

    # Define standard buckets explicitly
    daypart_defs = [
        {"daypart": "Morning (06:00-11:59)", "start": 6, "end": 11, "hours_span": 6},
        {"daypart": "Afternoon (12:00-16:59)", "start": 12, "end": 16, "hours_span": 5},
        {"daypart": "Evening (17:00-21:59)", "start": 17, "end": 21, "hours_span": 5},
        {"daypart": "Late Hours (22:00-05:59)", "start": 22, "end": 5, "hours_span": 8}
    ]

    daypart_rows = []
    for dp in daypart_defs:
        name = dp["daypart"]
        if dp["start"] <= dp["end"]:
            sub = df[(df["hour"] >= dp["start"]) & (df["hour"] <= dp["end"])]
        else:
            sub = df[(df["hour"] >= dp["start"]) | (df["hour"] <= dp["end"])]

        cnt = len(sub)
        units = sub["transaction_qty"].sum() if cnt > 0 else 0
        rev = sub["revenue"].sum() if cnt > 0 else 0.0
        atv = rev / cnt if cnt > 0 else 0.0

        daypart_rows.append({
            "daypart": name,
            "operating_window": f"{dp['start']:02d}:00 - {dp['end']:02d}:59" if dp["start"] <= dp["end"] else "22:00 - 05:59",
            "hours_span": dp["hours_span"],
            "transactions": cnt,
            "pct_transactions": (cnt / total_trans) * 100,
            "units_sold": units,
            "pct_units": (units / total_units) * 100,
            "total_revenue": round(rev, 2),
            "pct_revenue": (rev / total_rev) * 100,
            "atv": round(atv, 2),
            "trans_per_active_hour": round(cnt / dp["hours_span"], 1)
        })

    df_daypart = pd.DataFrame(daypart_rows)
    print(df_daypart.to_string(index=False, formatters={
        "transactions": "{:,}".format,
        "units_sold": "{:,}".format,
        "total_revenue": "${:,.2f}".format,
        "atv": "${:.2f}".format,
        "pct_transactions": "{:.2f}%".format,
        "pct_units": "{:.2f}%".format,
        "pct_revenue": "{:.2f}%".format,
        "trans_per_active_hour": "{:,.1f}".format
    }))

    daypart_csv_path = os.path.join(OUTPUT_DIR, "03_daypart_performance.csv")
    df_daypart.to_csv(daypart_csv_path, index=False)
    print(f"Saved: {daypart_csv_path}")

    # Module 4: Peak, Moderate, and Off-Peak Classification
    print("\n" + "=" * 60)
    print("MODULE 4: PEAK, MODERATE & OFF-PEAK CLASSIFICATION")
    print("=" * 60)

    tier_perf = df.groupby("demand_tier").agg(
        transactions=("transaction_id", "count"),
        units_sold=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum"),
        atv=("revenue", "mean"),
        distinct_hours=("hour", "nunique")
    ).reset_index()

    tier_perf["pct_transactions"] = (tier_perf["transactions"] / total_trans) * 100
    tier_perf["pct_revenue"] = (tier_perf["total_revenue"] / total_rev) * 100
    tier_perf["criteria"] = tier_perf["demand_tier"].map({
        "Peak": "Hourly volume > 10,000 transactions (Top Rush Hours: 07, 08, 09, 10)",
        "Moderate": "Hourly volume 7,000 - 10,000 transactions (Sustained Day Demand: 11 to 18)",
        "Off-Peak": "Hourly volume < 7,000 transactions during operating window (06, 19, 20)",
        "Closed": "Outside operating hours (21:00 to 05:59; 0 transactions)"
    })
    tier_perf["hours_list"] = tier_perf["demand_tier"].map({
        "Peak": "07:00, 08:00, 09:00, 10:00 (4 hours)",
        "Moderate": "11:00, 12:00, 13:00, 14:00, 15:00, 16:00, 17:00, 18:00 (8 hours)",
        "Off-Peak": "06:00, 19:00, 20:00 (3 hours)",
        "Closed": "21:00 - 05:59 (9 hours)"
    })

    # Order by Peak, Moderate, Off-Peak
    tier_order = {"Peak": 1, "Moderate": 2, "Off-Peak": 3, "Closed": 4}
    tier_perf["sort_key"] = tier_perf["demand_tier"].map(tier_order)
    tier_perf = tier_perf.sort_values(by="sort_key").drop(columns=["sort_key"]).reset_index(drop=True)

    print(tier_perf.to_string(index=False, columns=[
        "demand_tier", "distinct_hours", "transactions", "pct_transactions", "total_revenue", "pct_revenue", "atv", "hours_list"
    ], formatters={
        "transactions": "{:,}".format,
        "total_revenue": "${:,.2f}".format,
        "atv": "${:.2f}".format,
        "pct_transactions": "{:.2f}%".format,
        "pct_revenue": "{:.2f}%".format
    }))

    tier_csv_path = os.path.join(OUTPUT_DIR, "04_peak_offpeak_classification.csv")
    tier_perf.to_csv(tier_csv_path, index=False)
    print(f"Saved: {tier_csv_path}")

    # Module 8: Store-Specific Hourly Demand Dynamics
    print("\n" + "=" * 60)
    print("MODULE 8: STORE-SPECIFIC HOURLY DEMAND MATRIX")
    print("=" * 60)

    store_hourly = df.groupby(["store_location", "hour", "hour_label"]).agg(
        transactions=("transaction_id", "count"),
        units_sold=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum"),
        atv=("revenue", "mean")
    ).reset_index().sort_values(by=["store_location", "hour"]).reset_index(drop=True)

    matrix_csv_path = os.path.join(OUTPUT_DIR, "08_store_hourly_performance.csv")
    store_hourly.to_csv(matrix_csv_path, index=False)
    print(f"Saved: {matrix_csv_path}")

    # Pivot for clean cross-tabulation
    pivot_trans = df.pivot_table(index="hour_label", columns="store_location", values="transaction_id", aggfunc="count", fill_value=0)
    pivot_csv_path = os.path.join(OUTPUT_DIR, "08_store_hourly_transaction_pivot.csv")
    pivot_trans.to_csv(pivot_csv_path)
    print(f"Saved: {pivot_csv_path}")

    pivot_rev = df.pivot_table(index="hour_label", columns="store_location", values="revenue", aggfunc="sum", fill_value=0.0).round(2)
    pivot_rev_path = os.path.join(OUTPUT_DIR, "08_store_hourly_revenue_pivot.csv")
    pivot_rev.to_csv(pivot_rev_path)
    print(f"Saved: {pivot_rev_path}")


if __name__ == "__main__":
    run_time_analysis()
