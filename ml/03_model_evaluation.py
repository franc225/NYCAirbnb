import joblib
import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "outputs" / "ml"
MODEL_DIR = BASE_DIR / "outputs" / "models"

X_test = pd.read_csv(ML_DIR / "X_test.csv")
y_test = pd.read_csv(ML_DIR / "y_test.csv").squeeze("columns")

model_files = [
    "linear_regression.joblib",
    "random_forest.joblib",
    "gradient_boosting.joblib",
]

results = []

for model_file in model_files:
    model_name = model_file.replace(".joblib", "")
    pipeline = joblib.load(MODEL_DIR / model_file)

    preds = pipeline.predict(X_test)

    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))

    results.append({
        "model": model_name,
        "r2": r2,
        "mae": mae,
        "rmse": rmse
    })

results_df = pd.DataFrame(results).sort_values("rmse")
print(results_df)

print("\nBest model based on RMSE:")
print(results_df.iloc[0])