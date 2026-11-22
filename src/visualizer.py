"""
Visualization Module for Afficionado Coffee Roasters.
Generates 8 high-resolution (300 DPI) publication-quality charts for the internship project.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set aesthetic style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "Segoe UI"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.dpi"] = 300

CHARTS_DIR = "charts"
OUTPUTS_DIR = "outputs"
os.makedirs(CHARTS_DIR, exist_ok=True)

# Cohesive Palette
COLOR_PRIMARY = "#4A2E18"      # Deep Espresso
COLOR_SECONDARY = "#C87D32"    # Warm Caramel / Amber
COLOR_ACCENT = "#2563EB"       # Corporate Blue
COLOR_TEAL = "#0D9488"         # Dark Cyan / Teal
COLOR_LIGHT = "#F3F4F6"
COLOR_PEAK = "#DC2626"         # Crimson
COLOR_MODERATE = "#D97706"     # Amber
COLOR_OFFPEAK = "#10B981"      # Emerald


def chart_01_hourly_trends():
    df = pd.read_csv(os.path.join(OUTPUTS_DIR, "02_hourly_performance.csv"))
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(df))
    width = 0.55
    
    bars = ax1.bar(x, df["transactions"], width, color=COLOR_SECONDARY, alpha=0.85, label="Transactions (Count)")
    ax1.set_xlabel("Operating Hour", fontsize=12, fontweight="bold", labelpad=10)
    ax1.set_ylabel("Transaction Volume", color=COLOR_PRIMARY, fontsize=12, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=COLOR_PRIMARY)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{h:02d}:00" for h in df["hour"]], rotation=45, ha="right")
    ax1.yaxis.set_major_formatter("{x:,.0f}")
    ax1.set_ylim(0, 22000)
    
    # Highlight Peak Hours
    for idx, row in df.iterrows():
        if row["demand_tier"] == "Peak":
            bars[idx].set_color(COLOR_PRIMARY)
            ax1.text(idx, row["transactions"] + 350, f"{row['transactions']:,}", ha="center", va="bottom", fontsize=8, fontweight="bold", color=COLOR_PRIMARY)
    
    ax2 = ax1.twinx()
    line = ax2.plot(x, df["total_revenue"], color="#DC2626", linewidth=2.5, marker="o", markersize=6, label="Gross Revenue ($)")
    ax2.set_ylabel("Total Gross Revenue ($)", color="#DC2626", fontsize=12, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#DC2626")
    ax2.yaxis.set_major_formatter("${x:,.0f}")
    ax2.set_ylim(0, 105000)
    ax2.grid(False)
    
    plt.title("Afficionado Coffee Roasters: Hourly Transaction Volume & Gross Revenue (2025)\nHighlighting Morning Rush (07:00 – 10:59)", fontsize=14, fontweight="bold", pad=15)
    
    # Combined Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, ["Transactions (Peak: Espresso, Others: Amber)", "Revenue ($)"], loc="upper left", frameon=True)
    
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "01_hourly_sales_and_volume_trend.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def chart_02_daypart_performance():
    df = pd.read_csv(os.path.join(OUTPUTS_DIR, "03_daypart_performance.csv"))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Revenue by Daypart
    colors = [COLOR_PRIMARY, COLOR_SECONDARY, "#4B5563", "#9CA3AF"]
    labels = [row["daypart"] for _, row in df.iterrows()]
    
    bars1 = ax1.bar(labels, df["total_revenue"], color=colors, width=0.6)
    ax1.set_title("Gross Revenue by Unified Mentor Daypart", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Gross Revenue ($)", fontsize=11, fontweight="bold")
    ax1.yaxis.set_major_formatter("${x:,.0f}")
    ax1.set_xticks(range(len(labels)))
    ax1.set_xticklabels(labels, rotation=20, ha="right", fontsize=9)
    ax1.set_ylim(0, 450000)
    for b, rev, pct in zip(bars1, df["total_revenue"], df["pct_revenue"]):
        if rev > 0:
            ax1.text(b.get_x() + b.get_width()/2, rev + 6000, f"${rev:,.0f}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")
        else:
            ax1.text(b.get_x() + b.get_width()/2, 3000, "$0 (Closed)", ha="center", va="bottom", fontsize=8, color="#6B7280")
            
    # Right: Hourly Transaction Velocity (Transactions per Active Hour)
    bars2 = ax2.bar(labels, df["trans_per_active_hour"], color=colors, width=0.6)
    ax2.set_title("Customer Order Velocity (Transactions per Operating Hour)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Transactions per Operating Hour", fontsize=11, fontweight="bold")
    ax2.yaxis.set_major_formatter("{x:,.0f}")
    ax2.set_xticks(range(len(labels)))
    ax2.set_xticklabels(labels, rotation=20, ha="right", fontsize=9)
    ax2.set_ylim(0, 16000)
    for b, vel in zip(bars2, df["trans_per_active_hour"]):
        if vel > 0:
            ax2.text(b.get_x() + b.get_width()/2, vel + 250, f"{vel:,.1f} / hr", ha="center", va="bottom", fontsize=9, fontweight="bold")
        else:
            ax2.text(b.get_x() + b.get_width()/2, 150, "0.0 / hr", ha="center", va="bottom", fontsize=8, color="#6B7280")

    plt.suptitle("Unified Mentor Daypart Performance Breakdown (2025)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "02_daypart_performance_unified_mentor.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def chart_03_peak_moderate_offpeak():
    df = pd.read_csv(os.path.join(OUTPUTS_DIR, "04_peak_offpeak_classification.csv"))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tiers = df["demand_tier"]
    x = np.arange(len(tiers))
    width = 0.35
    
    c_map = [COLOR_PEAK, COLOR_MODERATE, COLOR_OFFPEAK]
    
    bars_t = ax.bar(x - width/2, df["pct_transactions"], width, label="% of Total Transactions", color=COLOR_PRIMARY, alpha=0.9)
    bars_r = ax.bar(x + width/2, df["pct_revenue"], width, label="% of Total Revenue", color=COLOR_SECONDARY, alpha=0.9)
    
    ax.set_title("Demand Tier Contribution: Peak vs. Moderate vs. Off-Peak Hours", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Empirical Demand Classification Tier", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_ylabel("Share of Total (%)", fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{t}\n({h})" for t, h in zip(df["demand_tier"], df["hours_list"])], fontsize=10)
    ax.yaxis.set_major_formatter("{x:.0f}%")
    ax.set_ylim(0, 60)
    ax.legend(frameon=True, fontsize=10)
    
    for b in bars_t:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, h + 1, f"{h:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold", color=COLOR_PRIMARY)
        
    for b in bars_r:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, h + 1, f"{h:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold", color=COLOR_SECONDARY)
        
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "03_peak_moderate_offpeak_distribution.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def chart_04_store_comparison():
    df = pd.read_csv(os.path.join(OUTPUTS_DIR, "05_store_performance.csv"))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    
    store_colors = ["#1E3A8A", "#D97706", "#059669"]
    
    # Revenue comparison
    bars = ax1.bar(df["store_location"], df["total_revenue"], color=store_colors, width=0.55)
    ax1.set_title("Gross Revenue by Store Location", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Total Gross Revenue ($)", fontsize=11, fontweight="bold")
    ax1.yaxis.set_major_formatter("${x:,.0f}")
    ax1.set_ylim(0, 270000)
    for b, rev, pct in zip(bars, df["total_revenue"], df["pct_revenue"]):
        ax1.text(b.get_x() + b.get_width()/2, rev + 3500, f"${rev:,.2f}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")
        
    # ATV & Units per Order
    x = np.arange(len(df))
    width = 0.35
    bars_atv = ax2.bar(x - width/2, df["atv"], width, label="Average Transaction Value ($)", color="#4A2E18")
    bars_qty = ax2.bar(x + width/2, df["avg_units_per_order"], width, label="Avg Units per Order", color="#C87D32")
    
    ax2.set_title("Average Transaction Value (ATV) & Basket Size", fontsize=12, fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(df["store_location"], fontsize=10, fontweight="bold")
    ax2.set_ylim(0, 6.0)
    ax2.legend(frameon=True, loc="upper right")
    
    for b in bars_atv:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 0.1, f"${h:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#4A2E18")
    for b in bars_qty:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 0.1, f"{h:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#C87D32")

    plt.suptitle("Store Benchmarking: Astoria vs. Hell's Kitchen vs. Lower Manhattan", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "04_store_revenue_and_atv_comparison.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def chart_05_category_pareto():
    df = pd.read_csv(os.path.join(OUTPUTS_DIR, "06_product_category_performance.csv"))
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(df))
    bars = ax1.bar(x, df["total_revenue"], color=COLOR_PRIMARY, width=0.6, alpha=0.9, label="Category Revenue ($)")
    ax1.set_title("Product Category Performance & Pareto Distribution (80/20 Rule)", fontsize=14, fontweight="bold", pad=15)
    ax1.set_xlabel("Product Category", fontsize=12, fontweight="bold", labelpad=10)
    ax1.set_ylabel("Total Gross Revenue ($)", color=COLOR_PRIMARY, fontsize=12, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(df["product_category"], rotation=30, ha="right", fontsize=10)
    ax1.yaxis.set_major_formatter("${x:,.0f}")
    ax1.set_ylim(0, 310000)
    
    for b, rev in zip(bars, df["total_revenue"]):
        ax1.text(b.get_x() + b.get_width()/2, rev + 3500, f"${rev:,.0f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
        
    # Secondary axis: Cumulative line
    ax2 = ax1.twinx()
    line = ax2.plot(x, df["cumulative_revenue_pct"], color="#DC2626", linewidth=2.5, marker="o", markersize=6, label="Cumulative Revenue (%)")
    ax2.axhline(80, color="#6B7280", linestyle="--", linewidth=1.2, label="80% Revenue Cutoff")
    ax2.set_ylabel("Cumulative Share of Revenue (%)", color="#DC2626", fontsize=12, fontweight="bold")
    ax2.yaxis.set_major_formatter("{x:.0f}%")
    ax2.set_ylim(0, 110)
    ax2.grid(False)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right", frameon=True)
    
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "05_product_category_pareto_distribution.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def chart_06_top_skus():
    df = pd.read_csv(os.path.join(OUTPUTS_DIR, "06_product_sku_performance.csv")).head(10)
    df = df.sort_values(by="total_revenue", ascending=True)
    
    fig, ax = plt.subplots(figsize=(11, 6))
    
    bars = ax.barh(df["product_detail"], df["total_revenue"], color=COLOR_SECONDARY, height=0.65, alpha=0.9)
    ax.set_title("Top 10 Revenue-Generating Menu Items (SKUs) in 2025", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Total Gross Revenue ($)", fontsize=12, fontweight="bold", labelpad=10)
    ax.xaxis.set_major_formatter("${x:,.0f}")
    ax.set_xlim(0, 30000)
    
    for b, rev, cat in zip(bars, df["total_revenue"], df["product_category"]):
        ax.text(rev + 350, b.get_y() + b.get_height()/2, f"${rev:,.2f}  ({cat})", ha="left", va="center", fontsize=8.5, fontweight="bold", color=COLOR_PRIMARY)
        
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "06_top_10_revenue_generating_products.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def chart_07_basket_size():
    df = pd.read_csv(os.path.join(OUTPUTS_DIR, "07_basket_size_distribution.csv"))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    
    # Transaction Share
    colors = [COLOR_PRIMARY, COLOR_SECONDARY, "#3B82F6", "#10B981", "#6B7280", "#9CA3AF"]
    labels = [f"{q} Unit(s)" for q in df["transaction_qty"]]
    
    bars1 = ax1.bar(labels, df["pct_transactions"], color=colors[:len(df)], width=0.55)
    ax1.set_title("Transaction Share by Order Quantity", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Share of Transactions (%)", fontsize=11, fontweight="bold")
    ax1.yaxis.set_major_formatter("{x:.0f}%")
    ax1.set_ylim(0, 70)
    for b, pct in zip(bars1, df["pct_transactions"]):
        ax1.text(b.get_x() + b.get_width()/2, pct + 1, f"{pct:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")
        
    # Revenue Share
    bars2 = ax2.bar(labels, df["pct_revenue"], color=colors[:len(df)], width=0.55)
    ax2.set_title("Revenue Contribution by Order Quantity", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Share of Gross Revenue (%)", fontsize=11, fontweight="bold")
    ax2.yaxis.set_major_formatter("{x:.0f}%")
    ax2.set_ylim(0, 60)
    for b, pct in zip(bars2, df["pct_revenue"]):
        ax2.text(b.get_x() + b.get_width()/2, pct + 1, f"{pct:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.suptitle("Basket Size Analysis: Purchasing Behavior via transaction_qty", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "07_basket_size_qty_distribution.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def chart_08_store_heatmap():
    pivot_df = pd.read_csv(os.path.join(OUTPUTS_DIR, "08_store_hourly_transaction_pivot.csv"), index_col="hour_label")
    
    fig, ax = plt.subplots(figsize=(9, 8))
    
    sns.heatmap(pivot_df, annot=True, fmt=",d", cmap="YlOrBr", cbar_kws={"label": "Transaction Count"}, ax=ax, linewidths=0.5)
    ax.set_title("Store-Specific Hourly Customer Traffic Heatmap (2025)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Store Location", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_ylabel("Operating Hour", fontsize=12, fontweight="bold")
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "08_store_hourly_demand_heatmap.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")


def generate_all_charts():
    print("Generating all 8 project visualizations...")
    chart_01_hourly_trends()
    chart_02_daypart_performance()
    chart_03_peak_moderate_offpeak()
    chart_04_store_comparison()
    chart_05_category_pareto()
    chart_06_top_skus()
    chart_07_basket_size()
    chart_08_store_heatmap()
    print("All 8 charts successfully generated and saved in 'charts/'.")


if __name__ == "__main__":
    generate_all_charts()
