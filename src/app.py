# pylint: disable=W1203
import json
import logging

import psycopg2

from src.ctr_entry import (
    CtrEntry,
    extract_best_ctr_entry_with_margin,
    extract_ctr_entries,
)
from src.definitions import logger

connection = psycopg2.connect(
    user="postgres",
    password="test123",
    host="postgresql-db",
    database="ctrchallenge",
    port=5432,
)


def write_to_database(ctr_entry: CtrEntry, margin: float) -> None:
    logger.info(f"Winner: {ctr_entry} with margin of {margin:.4f}")
    sql_string = "INSERT INTO ctr (test_id, content_id, winner_id, ctr, margin) values(%s, %s, %s, %s, %s);"
    with connection.cursor() as cur:
        cur.execute(
            sql_string,
            (
                ctr_entry.test_id,
                ctr_entry.content_id,
                ctr_entry.child_id,
                ctr_entry.ctr,
                margin,
            ),
        )
        connection.commit()


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
