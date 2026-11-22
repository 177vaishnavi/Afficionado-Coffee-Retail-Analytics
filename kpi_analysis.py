"""
KPI Analysis Module for Afficionado Coffee Roasters.
Computes overall baseline metrics, store-wise benchmarking, product hierarchy performance,
and basket size (units per transaction) distribution.
"""

import os
import pandas as pd
import numpy as np

OUTPUT_DIR = "outputs"


def run_kpi_analysis():
    # Load processed data
    data_path = os.path.join(OUTPUT_DIR, "cleaned_transactions.csv")
    if not os.path.exists(data_path):
        from data_loader import get_data
        df = get_data()
    else:
        df = pd.read_csv(data_path)

    total_trans = len(df)
    total_rev = df["revenue"].sum()
    total_units = df["transaction_qty"].sum()
    overall_atv = total_rev / total_trans
    avg_units_per_trans = total_units / total_trans
    avg_realized_price = total_rev / total_units

    print("=" * 60)
    print("MODULE 1: OVERALL BASELINE METRICS (2025)")
    print("=" * 60)
    print(f"Total Transactions:        {total_trans:,}")
    print(f"Total Gross Revenue:       ${total_rev:,.2f}")
    print(f"Total Units Sold:          {total_units:,}")
    print(f"Average Transaction Value: ${overall_atv:.2f}")
    print(f"Average Units/Transaction: {avg_units_per_trans:.2f}")
    print(f"Average Realized Price:    ${avg_realized_price:.2f}")

    # 1. Save 01_overall_kpis.csv
    kpi_records = [
        {"metric": "Total Transactions", "value": total_trans, "formatted": f"{total_trans:,}", "description": "Total unique customer transactions across all stores in 2025"},
        {"metric": "Total Gross Revenue", "value": round(total_rev, 2), "formatted": f"${total_rev:,.2f}", "description": "Total sales revenue (unit_price * transaction_qty)"},
        {"metric": "Total Units Sold", "value": total_units, "formatted": f"{total_units:,}", "description": "Total quantity of items sold"},
        {"metric": "Average Transaction Value (ATV)", "value": round(overall_atv, 2), "formatted": f"${overall_atv:.2f}", "description": "Mean revenue per transaction"},
        {"metric": "Average Units per Transaction", "value": round(avg_units_per_trans, 2), "formatted": f"{avg_units_per_trans:.2f}", "description": "Average basket size in units"},
        {"metric": "Average Realized Unit Price", "value": round(avg_realized_price, 2), "formatted": f"${avg_realized_price:.2f}", "description": "Total revenue divided by total units sold"},
        {"metric": "Total Operating Stores", "value": df["store_id"].nunique(), "formatted": f"{df['store_id'].nunique()}", "description": "Number of retail coffee shop locations"},
        {"metric": "Product Categories", "value": df["product_category"].nunique(), "formatted": f"{df['product_category'].nunique()}", "description": "Number of high-level product categories"},
        {"metric": "Product Types", "value": df["product_type"].nunique(), "formatted": f"{df['product_type'].nunique()}", "description": "Number of product sub-types"},
        {"metric": "Product SKUs (Details)", "value": df["product_detail"].nunique(), "formatted": f"{df['product_detail'].nunique()}", "description": "Distinct menu items/sizes offered"}
    ]
    df_kpi = pd.DataFrame(kpi_records)
    kpi_csv_path = os.path.join(OUTPUT_DIR, "01_overall_kpis.csv")
    df_kpi.to_csv(kpi_csv_path, index=False)
    print(f"Saved: {kpi_csv_path}")

    # 2. Store Performance
    print("\n" + "=" * 60)
    print("MODULE 5: STORE PERFORMANCE COMPARISON")
    print("=" * 60)
    store_perf = df.groupby(["store_id", "store_location"]).agg(
        transactions=("transaction_id", "count"),
        units_sold=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum"),
        atv=("revenue", "mean"),
        avg_units_per_order=("transaction_qty", "mean")
    ).reset_index()

    store_perf["pct_transactions"] = (store_perf["transactions"] / total_trans) * 100
    store_perf["pct_units"] = (store_perf["units_sold"] / total_units) * 100
    store_perf["pct_revenue"] = (store_perf["total_revenue"] / total_rev) * 100
    store_perf = store_perf.sort_values(by="total_revenue", ascending=False).reset_index(drop=True)

    print(store_perf.to_string(index=False, formatters={
        "transactions": "{:,}".format,
        "units_sold": "{:,}".format,
        "total_revenue": "${:,.2f}".format,
        "atv": "${:.2f}".format,
        "avg_units_per_order": "{:.2f}".format,
        "pct_transactions": "{:.2f}%".format,
        "pct_units": "{:.2f}%".format,
        "pct_revenue": "{:.2f}%".format
    }))
    store_csv_path = os.path.join(OUTPUT_DIR, "05_store_performance.csv")
    store_perf.to_csv(store_csv_path, index=False)
    print(f"Saved: {store_csv_path}")

    # 3. Product Performance Hierarchy
    print("\n" + "=" * 60)
    print("MODULE 6: PRODUCT HIERARCHY PERFORMANCE (CATEGORY LEVEL)")
    print("=" * 60)
    cat_perf = df.groupby("product_category").agg(
        transactions=("transaction_id", "count"),
        units_sold=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum"),
        atv=("revenue", "mean")
    ).reset_index()

    cat_perf["pct_transactions"] = (cat_perf["transactions"] / total_trans) * 100
    cat_perf["pct_units"] = (cat_perf["units_sold"] / total_units) * 100
    cat_perf["pct_revenue"] = (cat_perf["total_revenue"] / total_rev) * 100
    cat_perf = cat_perf.sort_values(by="total_revenue", ascending=False).reset_index(drop=True)
    cat_perf["cumulative_revenue_pct"] = cat_perf["pct_revenue"].cumsum()

    print(cat_perf.to_string(index=False, formatters={
        "transactions": "{:,}".format,
        "units_sold": "{:,}".format,
        "total_revenue": "${:,.2f}".format,
        "atv": "${:.2f}".format,
        "pct_transactions": "{:.2f}%".format,
        "pct_units": "{:.2f}%".format,
        "pct_revenue": "{:.2f}%".format,
        "cumulative_revenue_pct": "{:.2f}%".format
    }))
    cat_csv_path = os.path.join(OUTPUT_DIR, "06_product_category_performance.csv")
    cat_perf.to_csv(cat_csv_path, index=False)
    print(f"Saved: {cat_csv_path}")

    # Product Type Performance
    type_perf = df.groupby(["product_category", "product_type"]).agg(
        transactions=("transaction_id", "count"),
        units_sold=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum"),
        atv=("revenue", "mean")
    ).reset_index().sort_values(by="total_revenue", ascending=False).reset_index(drop=True)
    type_perf["pct_revenue"] = (type_perf["total_revenue"] / total_rev) * 100
    type_perf["cumulative_revenue_pct"] = type_perf["pct_revenue"].cumsum()
    type_csv_path = os.path.join(OUTPUT_DIR, "06_product_type_performance.csv")
    type_perf.to_csv(type_csv_path, index=False)
    print(f"Saved: {type_csv_path}")

    # Top SKUs (Product Detail)
    sku_perf = df.groupby(["product_category", "product_type", "product_detail", "unit_price"]).agg(
        transactions=("transaction_id", "count"),
        units_sold=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum")
    ).reset_index().sort_values(by="total_revenue", ascending=False).reset_index(drop=True)
    sku_perf["pct_revenue"] = (sku_perf["total_revenue"] / total_rev) * 100
    sku_perf["cumulative_revenue_pct"] = sku_perf["pct_revenue"].cumsum()
    sku_csv_path = os.path.join(OUTPUT_DIR, "06_product_sku_performance.csv")
    sku_perf.to_csv(sku_csv_path, index=False)
    print(f"Saved: {sku_csv_path}")

    # 4. Basket Size Analysis (strictly units per transaction)
    print("\n" + "=" * 60)
    print("MODULE 7: BASKET SIZE DISTRIBUTION (TRANSACTION_QTY)")
    print("=" * 60)
    basket_perf = df.groupby("transaction_qty").agg(
        transactions=("transaction_id", "count"),
        total_units=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum"),
        atv=("revenue", "mean")
    ).reset_index()
    basket_perf["pct_transactions"] = (basket_perf["transactions"] / total_trans) * 100
    basket_perf["pct_units"] = (basket_perf["total_units"] / total_units) * 100
    basket_perf["pct_revenue"] = (basket_perf["total_revenue"] / total_rev) * 100

    print(basket_perf.to_string(index=False, formatters={
        "transactions": "{:,}".format,
        "total_units": "{:,}".format,
        "total_revenue": "${:,.2f}".format,
        "atv": "${:.2f}".format,
        "pct_transactions": "{:.2f}%".format,
        "pct_units": "{:.2f}%".format,
        "pct_revenue": "{:.2f}%".format
    }))
    basket_csv_path = os.path.join(OUTPUT_DIR, "07_basket_size_distribution.csv")
    basket_perf.to_csv(basket_csv_path, index=False)
    print(f"Saved: {basket_csv_path}")


if __name__ == "__main__":
    run_kpi_analysis()
