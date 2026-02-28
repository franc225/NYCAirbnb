import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "00_load_check.py",
    "01_clean.py",
    "02_kpi_check.py",
    "03_star_schema.py",
    "04_star_check.py",
    "05_load_to_sqlite.py",
    "06_run_sql_validation.py",
]

def main():
    for script in SCRIPTS:
        script_path = BASE_DIR / script
        print("\n" + "=" * 80)
        print("Running:", script_path.name)
        print("=" * 80)

        result = subprocess.run([sys.executable, str(script_path)], cwd=str(BASE_DIR.parent))
        if result.returncode != 0:
            raise SystemExit(f"\n❌ Pipeline failed at {script_path.name} (exit {result.returncode})")

    print("\n✅ Pipeline completed successfully (00 → 05)")

if __name__ == "__main__":
    main()