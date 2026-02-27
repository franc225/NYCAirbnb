import pandas as pd
from pathlib import Path

INPUT = "data/AB_NYC_2019.csv"
OUTDIR = Path("outputs/cleaned")
OUTDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

# Remove duplicates
df = df.drop_duplicates()

# Remove invalid prices
df = df[df["price"] > 0]
df = df[df["price"] <= 1000]

# Fix review metrics
df["reviews_per_month"] = df["reviews_per_month"].fillna(0)
df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

# Create BI KPIs
df["estimated_booked_days"] = 365 - df["availability_365"]
df["estimated_revenue"] = df["price"] * df["estimated_booked_days"]
df["revenue_percentile"] = df["estimated_revenue"].rank(pct=True)
df["price_percentile"] = df["price"].rank(pct=True)

df["revenue_tier"] = pd.qcut(
    df["estimated_revenue"],
    q=4,
    labels=["Low", "Mid-Low", "Mid-High", "High"]
)

df["price_bucket"] = pd.cut(
    df["price"],
    bins=[0, 100, 200, 400, 1000],
    labels=["Budget", "Standard", "Premium", "Luxury"]
)

upper_cap = df["price"].quantile(0.99)
df = df[df["price"] <= upper_cap]

# Save
out_path = OUTDIR / "airbnb_nyc_2019_cleaned.csv"
df.to_csv(out_path, index=False)

print("New shape:", df.shape)
print("Saved to:", out_path)