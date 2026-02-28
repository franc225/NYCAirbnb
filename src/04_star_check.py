import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
STAR_DIR = BASE_DIR / "outputs" / "star_schema"

FACT_PATH = STAR_DIR / "fact_listing_2019.csv"
DIM_HOST_PATH = STAR_DIR / "dim_host.csv"
DIM_LOC_PATH = STAR_DIR / "dim_location.csv"
DIM_ROOM_PATH = STAR_DIR / "dim_room_type.csv"
DIM_LISTING_PATH = STAR_DIR / "dim_listing.csv"


def assert_no_nulls(df: pd.DataFrame, cols: list[str], name: str) -> None:
    null_counts = df[cols].isna().sum()
    bad = null_counts[null_counts > 0]
    if not bad.empty:
        raise ValueError(f"[{name}] Nulls found:\n{bad}")


def assert_unique(df: pd.DataFrame, col: str, name: str) -> None:
    dups = df.duplicated(subset=[col]).sum()
    if dups > 0:
        raise ValueError(f"[{name}] Duplicate keys in '{col}': {dups}")


def assert_fk_coverage(fact: pd.DataFrame, dim: pd.DataFrame, fk: str, dim_key: str, dim_name: str) -> None:
    missing = set(fact[fk].dropna().unique()) - set(dim[dim_key].unique())
    if missing:
        sample = list(missing)[:10]
        raise ValueError(
            f"[FK COVERAGE] '{fk}' has values not found in {dim_name}.{dim_key}. "
            f"Missing count={len(missing)} sample={sample}"
        )


def main():
    # ---------- Load ----------
    fact = pd.read_csv(FACT_PATH)
    dim_host = pd.read_csv(DIM_HOST_PATH)
    dim_loc = pd.read_csv(DIM_LOC_PATH)
    dim_room = pd.read_csv(DIM_ROOM_PATH)
    dim_listing = pd.read_csv(DIM_LISTING_PATH)

    print("Loaded:")
    print(" fact:", fact.shape)
    print(" dim_host:", dim_host.shape)
    print(" dim_location:", dim_loc.shape)
    print(" dim_room_type:", dim_room.shape)
    print(" dim_listing:", dim_listing.shape)

    # ---------- Basic schema checks ----------
    required_fact_cols = [
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
    missing_cols = [c for c in required_fact_cols if c not in fact.columns]
    if missing_cols:
        raise ValueError(f"[fact] Missing required columns: {missing_cols}")

    # ---------- Key uniqueness in dims ----------
    assert_unique(dim_host, "host_key", "dim_host")
    assert_unique(dim_loc, "location_key", "dim_location")
    assert_unique(dim_room, "room_type_key", "dim_room_type")
    assert_unique(dim_listing, "listing_key", "dim_listing")

    # ---------- Natural key uniqueness (sanity) ----------
    assert_unique(dim_host, "host_id", "dim_host")
    assert_unique(dim_listing, "id", "dim_listing")

    # ---------- Fact FK null checks ----------
    fk_cols = ["listing_key", "host_key", "location_key", "room_type_key"]
    assert_no_nulls(fact, fk_cols, "fact")

    # ---------- FK coverage (referential integrity) ----------
    assert_fk_coverage(fact, dim_host, "host_key", "host_key", "dim_host")
    assert_fk_coverage(fact, dim_loc, "location_key", "location_key", "dim_location")
    assert_fk_coverage(fact, dim_room, "room_type_key", "room_type_key", "dim_room_type")
    assert_fk_coverage(fact, dim_listing, "listing_key", "listing_key", "dim_listing")

    # ---------- Measure sanity checks ----------
    if (fact["price"] <= 0).any():
        raise ValueError("[fact] Found price <= 0 (should be filtered in cleaning).")

    if (fact["price"] > 1000).any():
        raise ValueError("[fact] Found price > 1000 (should be trimmed in cleaning).")

    if (fact["availability_365"] < 0).any() or (fact["availability_365"] > 365).any():
        raise ValueError("[fact] availability_365 out of [0, 365].")

    if (fact["estimated_booked_days"] < 0).any() or (fact["estimated_booked_days"] > 365).any():
        raise ValueError("[fact] estimated_booked_days out of [0, 365].")

    # Recompute revenue and compare (tolerate tiny float issues)
    recomputed = fact["price"] * fact["estimated_booked_days"]
    diff = (recomputed - fact["estimated_revenue"]).abs()
    if (diff > 1e-6).any():
        bad_count = (diff > 1e-6).sum()
        raise ValueError(f"[fact] estimated_revenue mismatch vs price*booked_days. Bad rows: {bad_count}")

    # Percentiles should be between 0 and 1
    for col in ["price_percentile", "revenue_percentile"]:
        if (fact[col] < 0).any() or (fact[col] > 1).any():
            raise ValueError(f"[fact] {col} out of [0, 1].")

    # ---------- Quick BI summaries ----------
    print("\nBI sanity:")
    print(" Median price:", float(fact["price"].median()))
    print(" Median booked days:", float(fact["estimated_booked_days"].median()))
    print(" Median revenue:", float(fact["estimated_revenue"].median()))

    # Optional: check distribution by borough via join
    borough_median = (
        fact.merge(dim_loc[["location_key", "neighbourhood_group"]], on="location_key", how="left")
            .groupby("neighbourhood_group")["estimated_revenue"]
            .median()
            .sort_values(ascending=False)
    )
    print("\nMedian estimated revenue by borough:")
    print(borough_median)

    print("\n✅ STAR SCHEMA CHECKS PASSED")


if __name__ == "__main__":
    main()