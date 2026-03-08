import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT = BASE_DIR / "outputs" / "cleaned" / "airbnb_nyc_2019_cleaned.csv"
OUTDIR = BASE_DIR / "outputs" / "ml"
OUTDIR.mkdir(parents=True, exist_ok=True)

TARGET = "estimated_revenue"

NUM_FEATURES = [
    "price",
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "availability_365",
    "calculated_host_listings_count",
]

CAT_FEATURES = [
    "room_type",
    "neighbourhood_group",
]

FEATURES = NUM_FEATURES + CAT_FEATURES

df = pd.read_csv(INPUT)

ml_df = df[FEATURES + [TARGET]].copy()

X = ml_df[FEATURES]
y = ml_df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

X_train.to_csv(OUTDIR / "X_train.csv", index=False)
X_test.to_csv(OUTDIR / "X_test.csv", index=False)
y_train.to_csv(OUTDIR / "y_train.csv", index=False)
y_test.to_csv(OUTDIR / "y_test.csv", index=False)

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)
print("ML dataset preparation complete.")