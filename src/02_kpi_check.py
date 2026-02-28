from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

df = pd.read_csv(OUTPUT_DIR / "cleaned" / "airbnb_nyc_2019_cleaned.csv")

print("Median price:", df["price"].median())
print("Median estimated booked days:", df["estimated_booked_days"].median())
print("Median estimated revenue:", df["estimated_revenue"].median())

print("\nTop 5 revenues:")
print(df["estimated_revenue"].sort_values(ascending=False).head())

print("\nRevenue by borough:")
print(df.groupby("neighbourhood_group")["estimated_revenue"].median())