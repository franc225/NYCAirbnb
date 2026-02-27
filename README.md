# NYCAirbnb

🏠 Airbnb NYC 2019 — Business Intelligence Analysis
📌 Project Overview

This project analyzes the New York City Airbnb 2019 dataset (Kaggle) using a structured Business Intelligence approach.

The objectives of this project are to:

Clean and validate raw listing data

Define business-oriented KPIs

Prepare a reusable BI-ready dataset

Establish a foundation for dimensional modeling

Enable dashboard integration in any BI tool

The focus is on data preparation, metric definition, and analytical rigor, rather than machine learning.

📊 Dataset

Source: AB_NYC_2019.csv (Kaggle)

Initial dataset:

48,895 listings

16 columns

After cleaning:

48,645 listings

18 columns

Each row represents one Airbnb listing in New York City (2019).

🧹 Data Cleaning Strategy

The following data preparation steps were applied:

Removed duplicate records

Removed invalid prices (price <= 0)

Trimmed extreme outliers (price > 1000)

Represents approximately 0.5% of the dataset

Improves stability of central tendency metrics

Replaced missing reviews_per_month values with 0

Converted last_review to datetime format

This approach ensures analytical consistency while preserving business realism.

📈 Business KPIs Created

To support BI analysis, the following calculated fields were introduced:

📅 Estimated Booked Days
estimated_booked_days = 365 - availability_365

Used as a proxy for occupancy.

💰 Estimated Revenue
estimated_revenue = price × estimated_booked_days

⚠ Important note:
This revenue metric is an approximation based on calendar availability.
It assumes full occupancy on unavailable days and may reflect host blocking behavior rather than actual bookings.

📊 Percentile Metrics

To manage distribution skew without removing high-end listings:

price_percentile

revenue_percentile

These fields allow trimmed analysis (e.g., excluding top 1%) while preserving full dataset integrity.

📌 Key Initial Findings

Median price: $105

Median estimated booked days: 321 days

Median estimated revenue: $25,550

Listings are heavily concentrated in:

Manhattan

Brooklyn

Entire home/apartment represents the majority of listings

The revenue distribution is highly skewed, reinforcing the importance of median-based analysis.

🏗 Modeling Strategy (Next Phase)

The next phase will transform the dataset into a reusable star schema independent of any specific BI tool.

Planned structure:

Fact table: listing metrics

Dimension tables: location, room type, host

This will allow integration with:

Power BI

Tableau

SQL-based analytics platforms

Any modern BI environment

🛠 Tech Stack

Python (Pandas)

VS Code

CSV-based data modeling

Future dashboard layer (Power BI or equivalent)

🎯 Business Objective

This project demonstrates:

Data cleaning best practices

KPI definition and justification

Outlier handling strategy

Revenue approximation logic

Preparation for dimensional modeling

BI-oriented analytical thinking

The objective is to build a tool-agnostic, BI-ready analytical dataset, not just perform exploratory analysis.

🚀 Next Steps

Implement dimensional modeling (star schema)

Develop executive dashboard

Add SQL examples

Provide structured business insights
