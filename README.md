# asset-lifecycle-stage-reporter

Report the lifecycle stage of each asset from its age: age in years = days since purchase / 365.25, life used % = age / expected life × 100 — NEW under 25%, IN SERVICE 25% to under 75%, AGING 75% to under 100%, END OF LIFE at 100% or more — END OF LIFE first, then AGING, IN SERVICE, NEW, highest life-used % first within a stage.

Sample input is included (sample.csv with four assets).

## How to run

```sh
python3 main.py sample.csv --as-of 2026-11-13
```

## Example output

```
LT-03 (Lenovo ThinkPad T14): END OF LIFE - 6.0 year(s) old, 120.6% of 5-year life used
LT-02 (HP EliteBook 840): END OF LIFE - 4.7 year(s) old, 116.6% of 4-year life used
LT-01 (Dell Latitude 5540): IN SERVICE - 1.5 year(s) old, 36.3% of 4-year life used
LT-04 (Dell OptiPlex 7090): NEW - 0.2 year(s) old, 4.0% of 5-year life used
END OF LIFE: 2
AGING: 0
IN SERVICE: 1
NEW: 1
```

Standard library only. Run the tests with `python3 -m unittest discover`.
