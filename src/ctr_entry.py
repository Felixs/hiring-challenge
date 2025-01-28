from dataclasses import dataclass
from functools import cached_property
from typing import List, Tuple

from src.definitions import logger
from src.errors import EmptyMessageException


@dataclass
class CtrEntry:
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


def extract_ctr_entries(sns_message: dict) -> List[CtrEntry]:
    # TODO: might want to add schema validation
    extracted_ctr_entries = []
    for variant in sns_message["variants"]:
        extracted_ctr_entries.append(
            CtrEntry(
                test_id=sns_message["test_id"],
                content_id=sns_message["content_id"],
                child_id=variant["id"],
                clicks=int(variant["clicks"]),
                views=int(variant["views"]),
                msg_timestamp=sns_message["msg_timestamp"],
            )
        )
    return extracted_ctr_entries


def extract_best_ctr_entry_with_margin(
    ctr_entries: List[CtrEntry],
) -> Tuple[CtrEntry, float]:
    sorted_ctr_entries = sorted(ctr_entries, reverse=True)
    if len(sorted_ctr_entries) == 0:
        raise EmptyMessageException()

    if len(sorted_ctr_entries) == 1:
        return sorted_ctr_entries[0], 0.0

    margin = calculate_ctr_margin(sorted_ctr_entries[0], sorted_ctr_entries[1])

    return sorted_ctr_entries[0], margin


def calculate_ctr_margin(winner: CtrEntry, second_best: CtrEntry) -> float:
    return ((100 / second_best.ctr) * winner.ctr) - 100
