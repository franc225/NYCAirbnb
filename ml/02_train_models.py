import joblib
import pandas as pd
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "outputs" / "ml"
MODEL_DIR = BASE_DIR / "outputs" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

X_train = pd.read_csv(ML_DIR / "X_train.csv")
y_train = pd.read_csv(ML_DIR / "y_train.csv").squeeze("columns")

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

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, NUM_FEATURES),
    ("cat", categorical_transformer, CAT_FEATURES)
])

models = {
    "linear_regression": LinearRegression(),
    "random_forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),
    "gradient_boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    ),
}

for model_name, model in models.items():
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, MODEL_DIR / f"{model_name}.joblib")
    print(f"Saved model: {model_name}")

print("Model training complete.")