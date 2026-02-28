import re
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "outputs" / "bi" / "nycairbnb.db"
SQL_PATH = BASE_DIR / "sql" / "06_db_validation_kpi.sql"


def strip_sql_comments(sql: str) -> str:
    # Remove /* ... */ block comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    # Remove -- ... end-of-line comments
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    return sql


def print_results(cursor, max_rows: int = 50):
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchmany(max_rows)

    if not rows:
        print("  (No rows returned)")
        return

    print("  | ".join(columns))
    print("  " + "-" * 80)
    for row in rows:
        print("  | ".join(str(v) for v in row))

    # If there are more rows, let user know
    if cursor.fetchone() is not None:
        print("  ... (more rows not shown)")


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    raw_sql = SQL_PATH.read_text(encoding="utf-8")
    cleaned_sql = strip_sql_comments(raw_sql)

    # Split into statements
    statements = [s.strip() for s in cleaned_sql.split(";") if s.strip()]

    for i, stmt in enumerate(statements, 1):
        print("\n" + "=" * 80)
        print(f"Query {i}")
        print("=" * 80)

        try:
            cursor.execute(stmt)

            if cursor.description is not None:
                print_results(cursor)
            else:
                conn.commit()
                print("  Executed successfully.")

        except Exception as e:
            print("  ❌ Error:", e)
            print("  Statement preview:", stmt[:200].replace("\n", " ") + ("..." if len(stmt) > 200 else ""))

    conn.close()
    print("\n✅ SQL validation complete.")


if __name__ == "__main__":
    main()