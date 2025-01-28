import unittest

from parameterized import parameterized

from src.ctr_entry import CtrEntry


class TestCtrEntry(unittest.TestCase):
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
