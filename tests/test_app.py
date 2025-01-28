import unittest

from src.app import extract_best_ctr_entry_with_margin
from src.ctr_entry import CtrEntry
from src.errors import EmptyMessageException


class TestApp(unittest.TestCase):
    def setUp(self):
        self.high_ctr = CtrEntry(views=100, clicks=90)
        self.mid_ctr = CtrEntry(views=100, clicks=20)
        self.low_ctr = CtrEntry(views=100, clicks=1)
        return super().setUp()

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
        self.assertAlmostEqual(margin, self.high_ctr.ctr - self.mid_ctr.ctr)

    def test_extract_best_ctr_entry_with_margin(self):
        ctr_entries = [self.high_ctr, self.mid_ctr, self.low_ctr]
        best_ctr_entry, margin = extract_best_ctr_entry_with_margin(ctr_entries)
        self.assertEqual(best_ctr_entry, self.high_ctr)
        self.assertAlmostEqual(margin, self.high_ctr.ctr - self.mid_ctr.ctr)
