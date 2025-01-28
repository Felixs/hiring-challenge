from dataclasses import dataclass
from functools import cached_property
from typing import List, Tuple

from src.definitions import logger
from src.errors import EmptyMessageException


@dataclass
class CtrEntry:
    """CTR testcase for one specfic clickpath"""

    test_id: str = "unknown"
    content_id: str = "unknown"
    child_id: int = -1
    clicks: int = 0
    views: int = 0
    msg_timestamp: str = "unknown"

    @cached_property
    def ctr(self) -> float:
        # TODO: float might be to inaccurate
        try:
            ctr = (self.clicks / self.views) * 100
            if ctr > 100:
                return 100.0

            return ctr
        except ZeroDivisionError:
            logger.exception("calculation with 0 views impossible, setting CTR to 0")
            return 0.0

    def __lt__(self, other):
        return self.ctr < other.ctr

    def __eq__(self, other):
        return self.ctr == other.ctr

    def __repr__(self):
        return f"For test {self.test_id} #{self.child_id} with {self.ctr:.4f}% CTR"


def parse_ctr_entries(message: dict) -> List[CtrEntry]:
    """Creates list of CtrEntries from given message

    Args:
        sns_message (dict): message to parse

    Returns:
        List[CtrEntry]: extracted list of CtrEntries
    """
    # TODO: add schema validation
    extracted_ctr_entries = []
    for variant in message["variants"]:
        extracted_ctr_entries.append(
            CtrEntry(
                test_id=message["test_id"],
                content_id=message["content_id"],
                child_id=variant["id"],
                clicks=int(variant["clicks"]),
                views=int(variant["views"]),
                msg_timestamp=message["msg_timestamp"],
            )
        )
    return extracted_ctr_entries


def extract_best_ctr_entry_with_margin(
    ctr_entries: List[CtrEntry],
) -> Tuple[CtrEntry, float]:
    """Extracts the best performing CtrEntry with margin to next best
       performing CtrEntry

    Args:
        ctr_entries (List[CtrEntry]): all valid ctr_entries from a testcase

    Raises:
        EmptyMessageException: raises in case of empty list

    Returns:
        Tuple[CtrEntry, float]: best performing CtrEntry and margin
    """
    sorted_ctr_entries = sorted(ctr_entries, reverse=True)
    if len(sorted_ctr_entries) == 0:
        raise EmptyMessageException()

    if len(sorted_ctr_entries) == 1:
        return sorted_ctr_entries[0], 0.0

    margin = calculate_ctr_margin(sorted_ctr_entries[0], sorted_ctr_entries[1])

    return sorted_ctr_entries[0], margin


def calculate_ctr_margin(first: CtrEntry, second: CtrEntry) -> float:
    """Given 2 CtrEntries calculates the relativ ctr margin

    Args:
        first (CtrEntry): first CtrEntry
        second (CtrEntry): second CtrEnrty

    Returns:
        float: percentage of difference based on the second enrtys crt
    """
    return ((100 / second.ctr) * first.ctr) - 100
