import unittest

from parameterized import parameterized

from src.ctr_entry import (
    CtrEntry,
    calculate_ctr_margin,
    extract_best_ctr_entry_with_margin,
)
from src.definitions import logger
from src.errors import EmptyMessageException


class TestCtrEntry(unittest.TestCase):
    def setUp(self):
        self.high_ctr = CtrEntry(views=100, clicks=90)
        self.mid_ctr = CtrEntry(views=100, clicks=20)
        self.low_ctr = CtrEntry(views=100, clicks=1)
        # disabeling logger output for testcases
        logger.disabled = True
        return super().setUp()

    @parameterized.expand(
        [
            (CtrEntry(views=100, clicks=10), 10.0, "happy path"),
            (CtrEntry(views=0, clicks=1), 0.0, "zero division"),
            (CtrEntry(views=1, clicks=0), 0.0, "zero clicks"),
            (CtrEntry(views=10, clicks=100), 100.0, "more clicks than views"),
        ]
    )
    def test_ctr_calculation(self, ctr_entry: CtrEntry, expected: float, message: str):
        self.assertEqual(ctr_entry.ctr, expected, message)

    def test_extract_best_ctr_entry_with_margin_empty_list(self):
        with self.assertRaises(EmptyMessageException):
            extract_best_ctr_entry_with_margin([])

    def test_extract_best_ctr_entry_with_margin_single_entry(self):
        ctr_entries = [self.high_ctr]
        best_ctr_entry, margin = extract_best_ctr_entry_with_margin(ctr_entries)
        self.assertEqual(best_ctr_entry, self.high_ctr)
        self.assertEqual(margin, 0.0)

    def test_extract_best_ctr_entry_with_margin_two_entries(self):
        ctr_entries = [self.high_ctr, self.mid_ctr]
        best_ctr_entry, margin = extract_best_ctr_entry_with_margin(ctr_entries)
        self.assertEqual(best_ctr_entry, self.high_ctr)
        self.assertAlmostEqual(
            margin, calculate_ctr_margin(self.high_ctr, self.mid_ctr)
        )

    def test_extract_best_ctr_entry_with_margin(self):
        ctr_entries = [self.high_ctr, self.mid_ctr, self.low_ctr]
        best_ctr_entry, margin = extract_best_ctr_entry_with_margin(ctr_entries)
        self.assertEqual(best_ctr_entry, self.high_ctr)
        self.assertAlmostEqual(
            margin, calculate_ctr_margin(self.high_ctr, self.mid_ctr)
        )

    @parameterized.expand(
        [
            (
                CtrEntry(views=100, clicks=10),
                CtrEntry(views=100, clicks=10),
                0.0,
                "zero margin",
            ),
            (
                CtrEntry(views=100, clicks=15),
                CtrEntry(views=100, clicks=10),
                50.0,
                "50% margin",
            ),
            (
                CtrEntry(views=100, clicks=20),
                CtrEntry(views=100, clicks=10),
                100.0,
                "100% margin",
            ),
            (
                CtrEntry(views=100, clicks=30),
                CtrEntry(views=100, clicks=10),
                200.0,
                "200% margin",
            ),
        ]
    )
    def test_calculate_ctr_margin(
        self,
        higher_ctr_entry: CtrEntry,
        lower_ctr_entry: CtrEntry,
        expected: float,
        message: str,
    ):
        self.assertEqual(
            calculate_ctr_margin(higher_ctr_entry, lower_ctr_entry), expected, message
        )
