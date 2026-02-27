import pandas as pd

df = pd.read_csv("outputs/cleaned/airbnb_nyc_2019_cleaned.csv")

print("Median price:", df["price"].median())
print("Median estimated booked days:", df["estimated_booked_days"].median())
print("Median estimated revenue:", df["estimated_revenue"].median())

print("\nTop 5 revenues:")
print(df["estimated_revenue"].sort_values(ascending=False).head())