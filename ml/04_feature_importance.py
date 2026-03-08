import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "outputs" / "models"
OUTDIR = BASE_DIR / "outputs" / "ml"
OUTDIR.mkdir(parents=True, exist_ok=True)

pipeline = joblib.load(MODEL_DIR / "random_forest.joblib")

preprocessor = pipeline.named_steps["preprocessor"]
model = pipeline.named_steps["model"]

feature_names = preprocessor.get_feature_names_out()
importances = model.feature_importances_

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values("importance", ascending=False)

print(importance_df.head(20))

importance_df.to_csv(OUTDIR / "feature_importance.csv", index=False)
print("\nSaved feature importance to outputs/ml/feature_importance.csv")