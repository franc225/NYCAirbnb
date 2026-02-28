🏠 NYCAirbnb

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11-blue" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458" />
  <img src="https://img.shields.io/badge/Status-In%20Progress-orange" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

Airbnb NYC 2019 — Business Intelligence Analysis

📌 Project Overview

This project analyzes the New York City Airbnb 2019 dataset (Kaggle) using a structured Business Intelligence methodology.

Objectives

Validate and clean raw listing data

Define and justify business-oriented KPIs

Create a reusable BI-ready analytical dataset

Establish a foundation for dimensional modeling

Enable integration with any BI platform

The focus is on data preparation, metric governance, and analytical rigor, rather than machine learning.

📂 Project Structure

NYCAirbnb/
│
├── src/
│   ├── 00_load_check.py
│   ├── 01_clean.py
│   └── 02_kpi_check.py
│   ├── 03_star_schema.py
│   └── 04_star_check.py
│
├── data/
│   └── AB_NYC_2019.csv
│
├── outputs/
│   └── cleaned/
│       └── airbnb_nyc_2019_cleaned.csv
│   └── star_schema/
│       ├── fact_listing_2019.csv
│       ├── dim_host.csv
│       ├── dim_location.csv
│       ├── dim_room_type.csv
│       └── dim_listing.csv
│
├── README.md
└── requirements.txt

▶️ How to Run

python src/00_load_check.py
python src/01_clean.py
python src/02_kpi_check.py
python src/03_star_schema.py
python src/04_star_check.py

📊 Dataset

Source: AB_NYC_2019.csv (Kaggle)

Initial dataset

48,895 listings

16 columns

After cleaning

48,645 listings

18 columns

Each row represents one Airbnb listing in New York City in 2019.

🧹 Data Cleaning Strategy

✔ Duplicate removal

Ensures entity-level uniqueness.

✔ Invalid price filtering

Removed listings where:
price <= 0

✔ Extreme outlier trimming

Removed listings where:
price > 1000

Represents ~0.5% of the dataset
Stabilizes central tendency metrics
Reduces distortion in revenue estimation

✔ Missing value handling

reviews_per_month → filled with 0
last_review → converted to datetime

This approach prioritizes analytical consistency while preserving business realism.

📈 Business KPIs Created

To enable structured BI analysis, the following calculated fields were introduced:

📅 Estimated Booked Days
estimated_booked_days = 365 - availability_365

💰 Estimated Revenue
estimated_revenue = price × estimated_booked_days

⚠ Important Note
This revenue metric is an approximation based on calendar availability.

It assumes:

Full occupancy on unavailable days

No seasonal pricing variation

No host-side blocking

It provides a comparative revenue indicator, not actual revenue.

📊 Percentile-Based Metrics

To manage skewed distributions without excluding premium listings:

price_percentile

revenue_percentile

These allow:

Trimmed analysis (e.g., excluding top 1%)

Robust segmentation

Outlier-aware dashboards

Preservation of full dataset integrity

🏗 Dimensional Modeling (Star Schema)

The cleaned dataset is transformed into a tool-agnostic star schema.

⭐ Fact Table

fact_listing_2019

Grain:
1 row = 1 listing (2019 snapshot)

Contains:

Price metrics

Availability metrics

Revenue metrics

Percentile indicators

🧱 Dimension Tables

dim_host

dim_location

dim_room_type

dim_listing

Each dimension uses surrogate keys to ensure BI compatibility and scalability.

✅ Star Schema Validation

04_star_check.py ensures:

Dimension key uniqueness

No null foreign keys in fact table

Referential integrity between fact and dimensions

Revenue calculation consistency

Percentile validity

Business metric sanity checks

This guarantees structural and analytical reliability before dashboard integration.

📌 Key Initial Findings

Median price: $105

Median estimated booked days: 321 days

Median estimated revenue: $25,550

Market structure insights

Listings are heavily concentrated in:

Manhattan

Brooklyn

Entire home/apartment represents the dominant listing type

Revenue distribution is strongly right-skewed

This reinforces the importance of median-based KPIs instead of averages.

🛠 Tech Stack

Python (Pandas)

VS Code

CSV-based intermediate storage

Future dashboard layer (Power BI or equivalent)

🎯 Business Objective

This project demonstrates:

Data validation discipline

KPI definition governance

Outlier handling strategy

Revenue proxy transparency

Star schema implementation

BI-oriented analytical modeling

The goal is to produce a reusable analytical asset, not just exploratory insights.

🚀 Next Steps

Load star schema into SQLite / Postgres

Provide SQL examples

Build executive dashboard

Add segmentation tiers (revenue buckets)

Publish business insight summary