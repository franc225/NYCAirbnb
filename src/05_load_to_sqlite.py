import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STAR_DIR = BASE_DIR / "outputs" / "star_schema"
OUTDIR = BASE_DIR / "outputs" / "bi"
OUTDIR.mkdir(parents=True, exist_ok=True)

DB_PATH = OUTDIR / "nycairbnb.db"

TABLES = {
    "dim_host": STAR_DIR / "dim_host.csv",
    "dim_location": STAR_DIR / "dim_location.csv",
    "dim_room_type": STAR_DIR / "dim_room_type.csv",
    "dim_listing": STAR_DIR / "dim_listing.csv",
    "fact_listing_2019": STAR_DIR / "fact_listing_2019.csv",
}

INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_fact_host_key ON fact_listing_2019(host_key);",
    "CREATE INDEX IF NOT EXISTS idx_fact_location_key ON fact_listing_2019(location_key);",
    "CREATE INDEX IF NOT EXISTS idx_fact_room_type_key ON fact_listing_2019(room_type_key);",
    "CREATE INDEX IF NOT EXISTS idx_fact_listing_key ON fact_listing_2019(listing_key);",
]


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()  # recreate clean DB each run

    conn = sqlite3.connect(DB_PATH)

    try:
        for table_name, csv_path in TABLES.items():
            df = pd.read_csv(csv_path)

            # normalize last_review to ISO for SQLite friendliness
            if "last_review" in df.columns:
                df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce").dt.strftime("%Y-%m-%d")

            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Loaded {table_name}: {df.shape}")

        cur = conn.cursor()
        for stmt in INDEXES:
            cur.execute(stmt)
        conn.commit()

        print("\n✅ SQLite BI database created:", DB_PATH)

    finally:
        conn.close()


if __name__ == "__main__":
    main()