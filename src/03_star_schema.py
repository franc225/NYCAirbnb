import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT = BASE_DIR / "outputs" / "cleaned" / "airbnb_nyc_2019_cleaned.csv"
OUTDIR = BASE_DIR / "outputs" / "star_schema"
OUTDIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(INPUT)

    # ---------- dim_room_type ----------
    dim_room_type = (
        df[["room_type"]]
        .drop_duplicates()
        .sort_values("room_type")
        .reset_index(drop=True)
    )
    dim_room_type["room_type_key"] = range(1, len(dim_room_type) + 1)

    df = df.merge(dim_room_type, on="room_type", how="left")

    # ---------- dim_location ----------
    dim_location = (
        df[["neighbourhood_group", "neighbourhood"]]
        .drop_duplicates()
        .sort_values(["neighbourhood_group", "neighbourhood"])
        .reset_index(drop=True)
    )
    dim_location["location_key"] = range(1, len(dim_location) + 1)

    df = df.merge(dim_location, on=["neighbourhood_group", "neighbourhood"], how="left")

    # ---------- dim_host ----------
    # host_id is already a natural key; we add a surrogate host_key for BI consistency
    dim_host = (
        df[["host_id", "host_name", "calculated_host_listings_count"]]
        .drop_duplicates(subset=["host_id"])
        .sort_values("host_id")
        .reset_index(drop=True)
    )
    dim_host["host_key"] = range(1, len(dim_host) + 1)

    df = df.merge(dim_host[["host_id", "host_key"]], on="host_id", how="left")

    # ---------- dim_listing (optional but recommended) ----------
    dim_listing = (
        df[["id", "name"]]
        .drop_duplicates(subset=["id"])
        .sort_values("id")
        .reset_index(drop=True)
    )
    dim_listing["listing_key"] = range(1, len(dim_listing) + 1)

    df = df.merge(dim_listing[["id", "listing_key"]], on="id", how="left")

    # ---------- fact table ----------
    fact_cols = [
        "listing_key",
        "host_key",
        "location_key",
        "room_type_key",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "reviews_per_month",
        "availability_365",
        "estimated_booked_days",
        "estimated_revenue",
        "price_percentile",
        "revenue_percentile",
        "last_review",
    ]

    fact = df[fact_cols].copy()

    # Ensure types
    fact["last_review"] = pd.to_datetime(fact["last_review"], errors="coerce")

    # ---------- save ----------
    dim_room_type.to_csv(OUTDIR / "dim_room_type.csv", index=False)
    dim_location.to_csv(OUTDIR / "dim_location.csv", index=False)
    dim_host.to_csv(OUTDIR / "dim_host.csv", index=False)
    dim_listing.to_csv(OUTDIR / "dim_listing.csv", index=False)
    fact.to_csv(OUTDIR / "fact_listing_2019.csv", index=False)

    print("Saved star schema to:", OUTDIR)
    print("Fact shape:", fact.shape)

if __name__ == "__main__":
    main()