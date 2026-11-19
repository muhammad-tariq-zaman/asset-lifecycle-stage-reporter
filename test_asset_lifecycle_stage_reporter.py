import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
import datetime
from main import report

AS_OF = datetime.date(2026, 11, 13)

def row(asset, model, purchased, life):
    return {"asset": asset, "model": model, "purchase_date": purchased,
            "expected_life_years": str(life)}

class TestLifecycleStages(unittest.TestCase):
    def test_new_asset(self):
        r = report([row("A-1", "Dell", "2026-11-13", 5)], AS_OF)
        self.assertEqual((r[0][3], r[0][4]), (0.0, "NEW"))

    def test_in_service_asset(self):
        r = report([row("A-1", "Dell", "2025-11-13", 2)], AS_OF)
        self.assertEqual(r[0][4], "IN SERVICE")

    def test_aging_asset(self):
        r = report([row("A-1", "Dell", "2023-11-13", 4)], AS_OF)
        self.assertEqual(r[0][4], "AGING")

    def test_end_of_life_asset(self):
        r = report([row("A-1", "Dell", "2022-11-13", 4)], AS_OF)
        self.assertEqual(r[0][4], "END OF LIFE")

    def test_end_of_life_first(self):
        r = report([row("A-1", "Dell", "2026-11-13", 5),
                    row("A-2", "HP", "2022-11-13", 4)], AS_OF)
        self.assertEqual(r[0][0], "A-2")

    def test_highest_used_first_within_stage(self):
        r = report([row("A-1", "Dell", "2022-11-13", 4),
                    row("A-2", "HP", "2020-11-13", 5)], AS_OF)
        self.assertEqual(r[0][0], "A-2")

    def test_age_years_computed(self):
        r = report([row("A-1", "Dell", "2025-11-13", 4)], AS_OF)
        self.assertAlmostEqual(r[0][2], 1.0, places=1)

    def test_empty_input(self):
        self.assertEqual(report([], AS_OF), [])
