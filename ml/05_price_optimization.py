import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "outputs" / "models"
OUTDIR = BASE_DIR / "outputs" / "ml"

pipeline = joblib.load(MODEL_DIR / "random_forest.joblib")

listing = {
    "price": 100,
    "minimum_nights": 2,
    "number_of_reviews": 25,
    "reviews_per_month": 1.2,
    "availability_365": 120,
    "calculated_host_listings_count": 1,
    "room_type": "Entire home/apt",
    "neighbourhood_group": "Brooklyn"
}

listing_df = pd.DataFrame([listing])

prices = np.arange(20, 400, 5)

results = []

for p in prices:

    listing_df["price"] = p

    revenue = pipeline.predict(listing_df)[0]

    results.append({
        "price": p,
        "predicted_revenue": revenue
    })

results_df = pd.DataFrame(results)

best_row = results_df.loc[results_df["predicted_revenue"].idxmax()]

print("\nOptimal price:")
print(best_row)

OUTDIR.mkdir(parents=True, exist_ok=True)
results_df.to_csv(OUTDIR / "price_optimization_curve.csv", index=False)

