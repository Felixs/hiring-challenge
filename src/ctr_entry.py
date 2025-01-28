from dataclasses import dataclass
from functools import cached_property

from src.definitions import logger


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
        return f"#{self.content_id} with {self.ctr}% CTR"
