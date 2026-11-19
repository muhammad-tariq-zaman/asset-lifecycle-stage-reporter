"""Report the lifecycle stage of each asset from its age.

Usage: python3 main.py assets.csv [--as-of 2026-11-13]
CSV columns: asset,model,purchase_date,expected_life_years.
Age in years = days since purchase / 365.25; life used % =
age / expected life * 100.
- NEW: under 25% of life used.
- IN SERVICE: 25% to under 75%.
- AGING: 75% to under 100%.
- END OF LIFE: 100% or more.
END OF LIFE first, then AGING, IN SERVICE, NEW; within a stage
the highest life-used % comes first.
"""
import argparse, csv, sys
from datetime import date

STAGE_ORDER = {"END OF LIFE": 0, "AGING": 1, "IN SERVICE": 2, "NEW": 3}

def report(rows, as_of=None):
    as_of = as_of or date.today()
    out = []
    for row in rows:
        purchased = date.fromisoformat(row["purchase_date"].strip())
        life = float(row["expected_life_years"])
        age_years = (as_of - purchased).days / 365.25
        used = age_years / life * 100 if life > 0 else 0.0
        if used < 25:
            stage = "NEW"
        elif used < 75:
            stage = "IN SERVICE"
        elif used < 100:
            stage = "AGING"
        else:
            stage = "END OF LIFE"
        out.append((row["asset"].strip(), row["model"].strip(),
                    round(age_years, 1), round(used, 1), stage, life))
    return sorted(out, key=lambda r: (STAGE_ORDER[r[4]], -r[3], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--as-of", default=None, help="reference date YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    with open(args.path, newline="", encoding="utf-8") as f:
        results = report(list(csv.DictReader(f)), as_of)
    for asset, model, age_years, used, stage, life in results:
        life_text = f"{life:g}-year"
        print(f"{asset} ({model}): {stage} - {age_years:.1f} year(s) old, "
              f"{used:.1f}% of {life_text} life used")
    for stage in ("END OF LIFE", "AGING", "IN SERVICE", "NEW"):
        count = sum(1 for *_, s, _ in results if s == stage)
        print(f"{stage}: {count}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
