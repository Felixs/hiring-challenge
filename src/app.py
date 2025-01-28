import json
import logging
from typing import List, Tuple

from src.ctr_entry import CtrEntry
from src.definitions import logger
from src.errors import EmptyMessageException


def extract_ctr_entries(sns_message: dict) -> List[CtrEntry]:
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

    margin = sorted_ctr_entries[0].ctr - sorted_ctr_entries[1].ctr

    return sorted_ctr_entries[0], margin


def write_to_database(ctr_entry: CtrEntry, margin: float) -> None:
    logger.info(f"Winner: {ctr_entry} with margin of {margin}")


def lambda_handler(event, context):
    logging.info("Startup")
    try:
        # TODO: what about multiple reconds in one event?
        sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
        ctr_entries = extract_ctr_entries(sns_message)
        best_ctr_entry, winning_margin = extract_best_ctr_entry_with_margin(ctr_entries)
        write_to_database(best_ctr_entry, winning_margin)
    except Exception:
        logger.exception(f"Failed to processing event {event}")
        return {"status": 522, "message": "Unprocessable Event"}

    return {"status": 200, "message": "OK"}
