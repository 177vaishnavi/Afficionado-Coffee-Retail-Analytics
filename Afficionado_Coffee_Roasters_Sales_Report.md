# Sales Trend and Time-Based Performance Analysis
## Afficionado Coffee Roasters (FY 2025)
**Internship Program:** Unified Mentor — Data Analytics Project 2  
**Dataset Analyzed:** `Afficionado Coffee Roasters.xlsx` (149,116 Transaction Records)  
**Execution Environment:** Python 3.14 | Pandas | NumPy | Matplotlib | Seaborn  
**Report Date:** November 20, 2026  

---

## Executive Summary

This project delivers a sales performance and intra-day temporal analysis for **Afficionado Coffee Roasters** across its three retail branch locations (*Astoria*, *Hell's Kitchen*, and *Lower Manhattan*). The investigation is based strictly on **149,116 verified transaction records** totaling **$698,812.33 in gross revenue** and **214,470 recorded units** during FY 2025.

### Key Performance Highlights:
* **Overall Business Metrics:** The dataset yields an Average Transaction Value (**ATV**) of **$4.69**, an average recorded quantity of **1.44 units per transaction record**, and an average realized price per unit of **$3.26**.
* **Intra-Day Temporal Distribution:** Recorded transaction activity is concentrated in the early half of the day. The **Morning daypart (06:00 – 11:59)** accounts for **54.82% of all transaction records** (81,751 records) and **55.56% of total gross revenue** ($388,288.67).
* **Peak Volume Window:** A 4-hour window from **07:00 to 10:59** accounts for **45.19% of all transaction records** (67,391 records) and **45.80% of total revenue** ($320,069.26). Peak hourly transaction volume reaches **18,545 records** between 10:00 and 10:59.
* **Balanced Store Distribution:** Total revenue is distributed across the three recorded store locations: **Hell's Kitchen** leads with **$236,511.17 (33.84%)**, followed by **Astoria** at **$232,243.91 (33.23%)** and **Lower Manhattan** at **$230,057.25 (32.92%)**. **Lower Manhattan** records the highest Average Transaction Value (**$4.81**) and the highest average quantity per transaction (**1.50 units**).
* **Core Menu Drivers (Pareto Distribution):** The top two categories—**Coffee** ($269,952.45; 38.63%) and **Tea** ($196,405.95; 28.11%)—generate **66.74% of total gross revenue**. Together with **Bakery** ($82,315.64; 11.78%), the top three categories generate **78.52% of total sales**.
* **Transaction Quantity Distribution (`transaction_qty`):** Single-unit transaction records represent **58.45% of total records** ($322,430.83), while two-unit records account for **39.33%** ($343,529.60). Together, 1- and 2-unit transaction records comprise **97.78% of all recorded transactions**.

---

## Data Integrity, Scope Limitations & Analytical Methodology

### 1. Data Limitation Disclosure
* **Absence of Calendar Dates:** The provided dataset `Afficionado Coffee Roasters.xlsx` contains a constant year attribute (`year = 2025`) and lacks a calendar date column (`transaction_date`), month, or day-of-week field.
* **Integrity Commitment:** In strict adherence to data integrity standards, **no synthetic calendar dates, weekdays, or months were invented or simulated**. Consequently, daily sales trends, weekly cycle comparisons, month-over-month growth, and weekday versus weekend performance cannot be empirically established and are excluded from this project.
* **Intra-Day Temporal Modeling:** Time-based performance is evaluated through **15 recorded operating hours (06:00 to 20:59)**, four **Unified Mentor standard dayparts**, and an **empirical peak/moderate/off-peak demand classification**.

### 2. Transaction Granularity & Quantity Clarification
* Every record in the dataset contains a unique `transaction_id` (149,116 unique IDs across 149,116 rows). 
* Each row represents an individual transaction item record rather than a consolidated multi-item transaction. Multi-product associations and product pairings cannot be established from this data structure.
* Purchased quantity is strictly evaluated using `transaction_qty`, which records between 1 and 8 units per transaction record.

### 3. Staffing Suggestions Boundary
* Store staffing headcount, employee schedules, labor costs, and operational logs are unavailable in the dataset.
* Recommendations are framed strictly as **demand-based suggestions**, using hourly transaction record volume as an operational proxy for workload rather than measured staffing requirements.

---

## Module 1: Overall Baseline & Key Performance Indicators (KPIs)

The baseline operational metrics for Afficionado Coffee Roasters in 2025 are summarized below:

| Metric | Formatted Value | Raw Value | Business Definition |
| :--- | :---: | :---: | :--- |
| **Total Transactions** | **149,116** | 149,116 | Total unique transaction records in the dataset |
| **Total Gross Revenue** | **$698,812.33** | 698,812.33 | Sum of `(unit_price * transaction_qty)` |
| **Total Units Sold** | **214,470** | 214,470 | Total units recorded across all transactions |
| **Average Transaction Value (ATV)** | **$4.69** | 4.686 | Total Revenue / Total Transactions |
| **Average Quantity per Transaction** | **1.44 units** | 1.438 | Total Units Sold / Total Transactions |
| **Average Realized Unit Price** | **$3.26** | 3.258 | Total Revenue / Total Units Sold |
| **Active Retail Stores** | **3** | 3 | Astoria, Hell's Kitchen, Lower Manhattan |
| **Product Categories** | **9** | 9 | High-level menu groupings |
| **Product Sub-Types** | **29** | 29 | Mid-level beverage and food classifications |
| **Unique Product SKUs** | **80** | 80 | Specific product descriptions and sizes offered |

*Source Data Table: [01_overall_kpis.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/01_overall_kpis.csv)*

---

## Module 2: Hourly Sales & Intra-Day Volume Trends

Recorded timestamps span 15 hours from **06:00:00 to 20:59:32**. Transaction volume increases rapidly after 06:00, reaches peak volume mid-morning, stabilizes through the afternoon, and tapers off into the evening.

| Operating Hour | Time Interval | Transactions | % Trans | Units Sold | Gross Revenue | % Revenue | Hourly ATV | Demand Tier |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **06** | 06:00 – 06:59 | 4,594 | 3.08% | 6,865 | $21,900.27 | 3.13% | $4.77 | Off-Peak |
| **07** | 07:00 – 07:59 | 13,428 | 9.01% | 19,449 | $63,526.47 | 9.09% | $4.73 | **Peak** |
| **08** | 08:00 – 08:59 | 17,654 | 11.84% | 25,197 | $82,699.87 | 11.83% | $4.68 | **Peak** |
| **09** | 09:00 – 09:59 | 17,764 | 11.91% | 25,370 | $85,169.53 | 12.19% | $4.79 | **Peak** |
| **10** | 10:00 – 10:59 | 18,545 | 12.44% | 26,713 | $88,673.39 | 12.69% | $4.78 | **Peak (Highest)** |
| **11** | 11:00 – 11:59 | 9,766 | 6.55% | 14,035 | $46,319.14 | 6.63% | $4.74 | Moderate |
| **12** | 12:00 – 12:59 | 8,708 | 5.84% | 12,690 | $40,192.79 | 5.75% | $4.62 | Moderate |
| **13** | 13:00 – 13:59 | 8,714 | 5.84% | 12,439 | $40,367.45 | 5.78% | $4.63 | Moderate |
| **14** | 14:00 – 14:59 | 8,933 | 5.99% | 12,907 | $41,304.74 | 5.91% | $4.62 | Moderate |
| **15** | 15:00 – 15:59 | 8,979 | 6.02% | 12,923 | $41,733.10 | 5.97% | $4.65 | Moderate |
| **16** | 16:00 – 16:59 | 9,093 | 6.10% | 12,881 | $41,122.75 | 5.88% | $4.52 | Moderate |
| **17** | 17:00 – 17:59 | 8,745 | 5.86% | 12,700 | $40,134.31 | 5.74% | $4.59 | Moderate |
| **18** | 18:00 – 18:59 | 7,498 | 5.03% | 10,826 | $34,286.20 | 4.91% | $4.57 | Moderate |
| **19** | 19:00 – 19:59 | 6,092 | 4.09% | 8,595 | $28,446.68 | 4.07% | $4.67 | Off-Peak |
| **20** | 20:00 – 20:59 | 603 | 0.40% | 880 | $2,935.64 | 0.42% | $4.87 | Off-Peak |

*Source Data Table: [02_hourly_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/02_hourly_performance.csv)*  
*Visual Chart: [01_hourly_sales_and_volume_trend.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/01_hourly_sales_and_volume_trend.png)*

### Hourly Observations:
1. **Morning Surge (07:00 – 10:59):** Transaction records increase from hour 06 (4,594 records) to hour 07 (13,428 records), maintaining elevated volume through hour 10 (18,545 records).
2. **Afternoon Stability (12:00 – 16:59):** Mid-day volume remains within a stable range of 8,700 to 9,100 transactions per hour, generating between $40,000 and $41,700 in hourly gross revenue.
3. **Evening Decrease (20:00 – 20:59):** Transaction records decrease to 603 during the final recorded operating hour.

---

## Module 3: Unified Mentor Prescribed Daypart Performance

Performance is aggregated into the four prescribed time intervals:

| Daypart Name | Time Interval | Active Hours | Transactions | % Trans | Units Sold | Gross Revenue | % Revenue | ATV | Trans / Active Hr |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Morning** | **06:00 – 11:59** | 6 | **81,751** | **54.82%** | **117,629** | **$388,288.67** | **55.56%** | **$4.75** | **13,625.2** |
| **Afternoon** | **12:00 – 16:59** | 5 | **44,427** | **29.79%** | **63,840** | **$204,720.83** | **29.30%** | **$4.61** | **8,885.4** |
| **Evening** | **17:00 – 21:59** | 5 | **22,938** | **15.38%** | **33,001** | **$105,802.83** | **15.14%** | **$4.61** | **4,587.6** |
| **Late Hours** | **22:00 – 05:59** | 8 | **0** | **0.00%** | **0** | **$0.00** | **0.00%** | **$0.00** | **0.0** |

*Source Data Table: [03_daypart_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/03_daypart_performance.csv)*  
*Visual Chart: [02_daypart_performance_unified_mentor.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/02_daypart_performance_unified_mentor.png)*

### Critical Daypart Takeaways:
* **Morning Concentration:** The 6-hour morning window accounts for more than half of all transactions (54.82%) and total revenue (55.56%), with an average hourly volume of **13,625.2 transaction records**.
* **Afternoon Contribution:** The afternoon window generates 29.30% of gross revenue across 44,427 transactions.
* **Late Hours:** No transactions were recorded during the 22:00 to 05:59 interval in the dataset.

---

## Module 4: Peak, Moderate & Off-Peak Operational Classification

Using the empirical distribution of hourly transaction counts across the 15 recorded hours (mean = 9,941 transactions/hour), hours are classified into three operational tiers:

```text
       Demand Distribution by Operating Tiers
       ====================================================
       Peak Hours (07-10):     [45.19% of Volume]  (>10,000 / hr)
       Moderate Hours (11-18): [47.24% of Volume]  (7,000 - 10,000 / hr)
       Off-Peak Hours (06,19,20): [7.57% of Volume] (<7,000 / hr)
```

| Demand Tier | Empirical Cutoff Threshold | Operating Hours Included | Hours Count | Total Transactions | % of Total Trans | Gross Revenue | % of Total Revenue | Tier ATV |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Peak** | **$> 10,000$ transactions/hr** | 07:00, 08:00, 09:00, 10:00 | 4 | **67,391** | **45.19%** | **$320,069.26** | **45.80%** | **$4.75** |
| **Moderate** | **$7,000 - 10,000$ transactions/hr** | 11:00, 12:00, 13:00, 14:00, 15:00, 16:00, 17:00, 18:00 | 8 | **70,436** | **47.24%** | **$325,460.48** | **46.57%** | **$4.62** |
| **Off-Peak** | **$< 7,000$ transactions/hr** | 06:00, 19:00, 20:00 | 3 | **11,289** | **7.57%** | **$53,282.59** | **7.62%** | **$4.72** |
| **No Transactions** | No records present | 21:00 – 05:59 | 9 | 0 | 0.00% | $0.00 | 0.00% | $0.00 |

*Source Data Table: [04_peak_offpeak_classification.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/04_peak_offpeak_classification.csv)*  
*Visual Chart: [03_peak_moderate_offpeak_distribution.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/03_peak_moderate_offpeak_distribution.png)*

### Classification Rationale:
* **Peak Tier:** Comprises 4 hours (26.7% of the active hours) and accounts for **45.19% of all transactions**, averaging **16,848 transactions per hour**.
* **Moderate Tier:** Comprises 8 hours and accounts for **47.24% of transactions**, averaging **8,805 transactions per hour**.
* **Off-Peak Tier:** Represents the remaining **7.57% of transactions**, covering the early opening hour (06:00) and evening hours (19:00–20:59).

---

## Module 5: Store-Wise Performance Comparison

Afficionado operates three store locations. Gross revenue and transaction volume are distributed evenly across the three branches:

| Store ID | Location | Transactions | % Trans | Units Sold | % Units | Gross Revenue | % Revenue | ATV | Avg Units / Trans |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **8** | **Hell's Kitchen** | 50,735 | 34.02% | 71,737 | 33.45% | **$236,511.17** | **33.84%** | $4.66 | 1.41 |
| **3** | **Astoria** | 50,599 | 33.93% | 70,991 | 33.10% | **$232,243.91** | **33.23%** | $4.59 | 1.40 |
| **5** | **Lower Manhattan** | 47,782 | 32.04% | 71,742 | 33.45% | **$230,057.25** | **32.92%** | **$4.81** | **1.50** |

*Source Data Table: [05_store_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/05_store_performance.csv)*  
*Visual Chart: [04_store_revenue_and_atv_comparison.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/04_store_revenue_and_atv_comparison.png)*

### Store Insights:
1. **Hell's Kitchen** accounts for the highest transaction count (50,735) and gross revenue ($236,511.17).
2. **Astoria** records 50,599 transactions and $232,243.91 in gross revenue, with an ATV of $4.59.
3. **Lower Manhattan** records 47,782 transactions but achieves the **highest ATV ($4.81)** and highest average units per transaction (**1.50**), resulting in total units sold (71,742) comparable to Hell's Kitchen (71,737).

---

## Module 6: Product Portfolio Performance & 80/20 Pareto Analysis

### Category-Level Performance (9 Categories)

| Product Category | Transactions | % Trans | Units Sold | % Units | Total Gross Revenue | % Revenue | Cumul % Rev | Category ATV |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Coffee** | 58,416 | 39.17% | 89,250 | 41.61% | **$269,952.45** | **38.63%** | 38.63% | $4.62 |
| **Tea** | 45,449 | 30.48% | 69,737 | 32.52% | **$196,405.95** | **28.11%** | 66.74% | $4.32 |
| **Bakery** | 22,796 | 15.29% | 23,214 | 10.82% | **$82,315.64** | **11.78%** | **78.52%** | $3.61 |
| **Drinking Chocolate** | 11,468 | 7.69% | 17,457 | 8.14% | **$72,416.00** | **10.36%** | **88.88%** | $6.31 |
| **Coffee beans** | 1,753 | 1.18% | 1,828 | 0.85% | **$40,085.25** | **5.74%** | 94.61% | $22.87 |
| **Branded** | 747 | 0.50% | 776 | 0.36% | **$13,607.00** | **1.95%** | 96.56% | $18.22 |
| **Loose Tea** | 1,210 | 0.81% | 1,210 | 0.56% | **$11,213.60** | **1.60%** | 98.17% | $9.27 |
| **Flavours** | 6,790 | 4.55% | 10,511 | 4.90% | **$8,408.80** | **1.20%** | 99.37% | $1.24 |
| **Packaged Chocolate**| 487 | 0.33% | 487 | 0.23% | **$4,407.64** | **0.63%** | 100.00% | $9.05 |

*Source Data Table: [06_product_category_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/06_product_category_performance.csv)*  
*Visual Chart: [05_product_category_pareto_distribution.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/05_product_category_pareto_distribution.png)*

### Category Observations:
* **Pareto Concentration:** The top 4 categories (**Coffee, Tea, Bakery, Drinking Chocolate**) account for **88.88% of total gross revenue**.
* **Higher Unit Price Categories:** **Coffee beans** accounts for 1.18% of transactions but yields an ATV of **$22.87**, generating $40,085.25 in total sales. Similarly, **Branded** goods average $18.22 per transaction.

---

### Top 10 Revenue-Generating Menu Items (SKUs)

| Rank | Product Detail / SKU Name | Product Category | Product Type | Unit Price | Total Units Sold | Total Gross Revenue | % Total Rev |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | **Barista Espresso Lg** | Coffee | Barista Espresso | $4.25 | 6,692 | **$28,441.00** | 4.07% |
| **2** | **Dark Chocolate Lg** | Drinking Chocolate | Hot chocolate | $4.50 | 5,528 | **$24,876.00** | 3.56% |
| **3** | **Sustainably Grown Organic Lg**| Coffee | Gourmet brewed coffee | $4.25 | 5,595 | **$23,778.75** | 3.40% |
| **4** | **Earl Grey Lg** | Tea | Brewed Black tea | $3.75 | 6,051 | **$22,691.25** | 3.25% |
| **5** | **Latte Lg** | Coffee | Barista Espresso | $4.25 | 5,291 | **$22,486.75** | 3.22% |
| **6** | **Cappuccino Lg** | Coffee | Barista Espresso | $4.25 | 5,283 | **$22,452.75** | 3.21% |
| **7** | **English Breakfast Lg** | Tea | Brewed Black tea | $3.75 | 5,836 | **$21,885.00** | 3.13% |
| **8** | **Serenity Green Tea Lg** | Tea | Brewed Green tea | $3.75 | 5,790 | **$21,712.50** | 3.11% |
| **9** | **Morning Sunrise Chai Lg** | Tea | Brewed Chai tea | $3.75 | 5,773 | **$21,648.75** | 3.10% |
| **10**| **Columbian Medium Roast Lg** | Coffee | Gourmet brewed coffee | $3.75 | 5,765 | **$21,618.75** | 3.09% |

*Source Data Table: [06_product_sku_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/06_product_sku_performance.csv)*  
*Visual Chart: [06_top_10_revenue_generating_products.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/06_top_10_revenue_generating_products.png)*

### SKU Observations:
* **Item-Level Contribution:** All 10 top-ranking SKUs by total gross revenue are Large ("Lg") size items, with unit prices ranging between $3.75 and $4.50. Together, these 10 items generate **$230,791.50**, representing **33.03% of total company gross revenue**.

---

## Module 7: Transaction Quantity Distribution (`transaction_qty`)

Because each record represents an individual line item, quantity purchased is analyzed directly via `transaction_qty`:

| Quantity per Record (`transaction_qty`) | Transactions | % of Total Trans | Total Units Sold | % of Total Units | Gross Revenue | % of Total Revenue | Mean Revenue / Trans |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 unit** | **87,159** | **58.45%** | 87,159 | 40.64% | $322,430.83 | 46.14% | $3.70 |
| **2 units** | **58,642** | **39.33%** | 117,284 | 54.69% | $343,529.60 | 49.16% | $5.86 |
| **3 units** | **3,279** | **2.20%** | 9,837 | 4.59% | $28,829.10 | 4.13% | $8.79 |
| **4 units** | **23** | **0.02%** | 92 | 0.04% | $206.80 | 0.03% | $8.99 |
| **6 units** | **3** | **0.00%** | 18 | 0.01% | $216.00 | 0.03% | $72.00 |
| **8 units** | **10** | **0.01%** | 80 | 0.04% | $3,600.00 | 0.52% | $360.00 |

*Source Data Table: [07_basket_size_distribution.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/07_basket_size_distribution.csv)*  
*Visual Chart: [07_basket_size_qty_distribution.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/07_basket_size_qty_distribution.png)*

### Quantity Distribution Takeaways:
* **Concentration in 1–2 Units:** **97.78% of all transaction records reflect 1 or 2 units**. Single-unit records account for 58.45% of transactions (87,159 records), while two-unit records account for 39.33% (58,642 records) and the largest share of revenue (49.16%).
* **Higher Quantity Records:** Transactions with quantities of 3, 4, 6, and 8 units occur infrequently (accounting for 2.22% of total transactions combined), with 8-unit records generating an average transaction value of $360.00.

---

## Module 8: Store-Specific Hourly Demand Dynamics

Cross-tabulating transaction volume across store locations and recorded hours highlights intra-day patterns across the three branches:

```text
Store Hourly Transaction Matrix (06:00 to 20:59)
Hour Interval      Astoria (Store 3)    Hell's Kitchen (Store 8)    Lower Manhattan (Store 5)
06:00 - 06:59            1,570                   1,532                        1,492
07:00 - 07:59            4,524                   4,611                        4,293
08:00 - 08:59            6,013                   6,063                        5,578
09:00 - 09:59            6,112                   6,068                        5,584
10:00 - 10:59            6,339                   6,290                        5,916
11:00 - 11:59            3,251                   3,356                        3,159
12:00 - 12:59            2,987                   2,912                        2,809
13:00 - 13:59            2,994                   2,971                        2,749
14:00 - 14:59            3,025                   3,040                        2,868
15:00 - 15:59            3,061                   3,042                        2,876
16:00 - 16:59            3,071                   3,115                        2,907
17:00 - 17:59            2,987                   2,965                        2,793
18:00 - 18:59            2,543                   2,525                        2,430
19:00 - 19:59            2,060                   2,036                        1,996
20:00 - 20:59               62                     209                          332
```

*Source Data Tables: [08_store_hourly_transaction_pivot.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/08_store_hourly_transaction_pivot.csv) | [08_store_hourly_revenue_pivot.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/08_store_hourly_revenue_pivot.csv)*  
*Visual Chart: [08_store_hourly_demand_heatmap.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/08_store_hourly_demand_heatmap.png)*

### Store Demand Observations:
1. **Synchronized Peak Hours:** All three stores record their highest transaction volumes between 08:00 and 10:59, each recording over 5,500 to 6,300 transactions per hour during this window.
2. **Late Evening Difference:** In the 20:00–20:59 interval, Lower Manhattan records 332 transactions, compared to 209 in Hell's Kitchen and 62 in Astoria.

---

## Strategic Business & Operational Recommendations

### 1. Demand-Based Labor Allocation Suggestions (Hypothetical Workload Proxy)
> [!NOTE]
> **Methodology Clarification:** Employee headcount, shift schedules, labor costs, and operational audits are not present in the dataset. The following points represent hypothetical, demand-based suggestions derived strictly from recorded hourly transaction volume as an operational workload proxy, rather than measured staffing requirements.

* **Peak Tier Allocation (07:00 – 10:59):** This 4-hour window accounts for 45.19% of all transaction records, with system-wide hourly volume exceeding 13,000 to 18,500 records (~4,300 to 6,300 per store location). Workstation planning could prioritize maximum coverage across transaction processing, beverage preparation, and product dispatch to accommodate this recorded volume.
* **Moderate Tier Allocation (11:00 – 18:59):** Transaction volume stabilizes at an average of ~8,800 records per hour system-wide (~2,800 to 3,300 per store location). This predictable volume profile provides a suitable window for standard shift rotations, restocking, and prep work without conflicting with peak transaction flow.
* **Off-Peak Allocation (06:00 & 19:00 – 20:59):** Volume averages under 4,600 records system-wide at opening (06:00) and decreases below 1,000 records across stores in the 20:00 hour, suggesting that minimal coverage is needed relative to midday hours.

### 2. Daypart Commercial Strategy
* **Morning Combinations (06:00 – 11:59):** Given that Bakery represents 11.78% of sales and single-unit records represent 58.45% of transactions, promotional combinations (e.g., beverage plus bakery item) could be tested to encourage multi-unit transactions during morning hours.
* **Afternoon Menu Focus (12:00 – 16:59):** The afternoon window contributes 29.30% of total revenue. Featuring specialty teas and cold beverages during this time could support volume during the mid-day plateau.

### 3. Product Mix Observations
* **Large Size Representation:** The top 10 SKUs by gross revenue are all Large size items ($3.75 to $4.50). Maintaining consistent inventory of large cups, lids, and corresponding ingredient proportions is directly supported by this sales volume.
* **Packaged Coffee Merchandising:** Coffee Beans generate an average transaction value of $22.87 across 1,753 transactions. Maintaining visible shelf displays for packaged beans at retail counters could help sustain these higher-value transactions.

---

## Project Repository & Deliverables Catalog

All analysis files and figures have been generated and archived in the project workspace:

### Python Analysis Code (`src/`):
* [data_loader.py](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/src/data_loader.py) — Data loading, schema validation, feature engineering, and cleaned dataset export.
* [kpi_analysis.py](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/src/kpi_analysis.py) — Baseline business KPIs, store benchmarking, product hierarchy, and quantity distribution.
* [time_analysis.py](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/src/time_analysis.py) — Hourly trends, Unified Mentor dayparts, peak/off-peak classification, and store hourly matrix.
* [visualizer.py](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/src/visualizer.py) — High-resolution visualization engine (300 DPI).

### Cleaned & Summary Data Tables (`outputs/`):
* [cleaned_transactions.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/cleaned_transactions.csv) — Feature-engineered dataset (20.6 MB, 149,116 rows).
* [01_overall_kpis.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/01_overall_kpis.csv) — Baseline performance KPIs.
* [02_hourly_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/02_hourly_performance.csv) — Hour-by-hour sales and transaction breakdown.
* [03_daypart_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/03_daypart_performance.csv) — Unified Mentor dayparts summary.
* [04_peak_offpeak_classification.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/04_peak_offpeak_classification.csv) — Empirical operating tier thresholds and volumes.
* [05_store_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/05_store_performance.csv) — Store benchmarking metrics.
* [06_product_category_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/06_product_category_performance.csv) — Category-level sales and Pareto cumulative percentages.
* [06_product_type_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/06_product_type_performance.csv) — Product type performance.
* [06_product_sku_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/06_product_sku_performance.csv) — Item-level (SKU) performance.
* [07_basket_size_distribution.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/07_basket_size_distribution.csv) — Quantity per transaction record frequency breakdown.
* [08_store_hourly_performance.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/08_store_hourly_performance.csv) — Store by hour granular table.
* [08_store_hourly_transaction_pivot.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/08_store_hourly_transaction_pivot.csv) — Cross-tabulated transaction pivot.
* [08_store_hourly_revenue_pivot.csv](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/outputs/08_store_hourly_revenue_pivot.csv) — Cross-tabulated revenue pivot.

### Publication-Quality Charts (`charts/`):
* [01_hourly_sales_and_volume_trend.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/01_hourly_sales_and_volume_trend.png)
* [02_daypart_performance_unified_mentor.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/02_daypart_performance_unified_mentor.png)
* [03_peak_moderate_offpeak_distribution.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/03_peak_moderate_offpeak_distribution.png)
* [04_store_revenue_and_atv_comparison.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/04_store_revenue_and_atv_comparison.png)
* [05_product_category_pareto_distribution.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/05_product_category_pareto_distribution.png)
* [06_top_10_revenue_generating_products.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/06_top_10_revenue_generating_products.png)
* [07_basket_size_qty_distribution.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/07_basket_size_qty_distribution.png)
* [08_store_hourly_demand_heatmap.png](file:///c:/Users/vaish/Desktop/Afficionado_Coffee_Sales_Analysis/charts/08_store_hourly_demand_heatmap.png)

---
*Report revised, verified, and finalized for Unified Mentor Internship submission.*
