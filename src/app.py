# pylint: disable=W1203
import json
import logging
import os

import psycopg2

from src.ctr_entry import (
    CtrEntry,
    extract_best_ctr_entry_with_margin,
    extract_ctr_entries,
)
from src.definitions import logger

# TODO: read connection secret
connection = psycopg2.connect(
    user=os.environ.get("DATABASE_USER", "postgres"),
    password=os.environ.get("DATABASE_PASSWORD", ""),
    host=os.environ.get("DATABASE_HOST", "postgresql-db"),
    database=os.environ.get("DATABASE_DB_NAME", "ctrchallenge"),
    port=int(os.environ.get("DATABASE_PORT", "5432")),
)


def write_to_database(ctr_entry: CtrEntry, margin: float) -> None:
    sql_string = "INSERT INTO ctr (test_id, content_id, winner_id, ctr_percent, margin_percent) values(%s, %s, %s, %s, %s);"
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

        logger.info(f"Winner: {best_ctr_entry} with margin of {winning_margin:.4f}")
    except Exception:
        logger.exception(f"Failed to processing event {event}")
        # TODO: message monitoring or write error output somewhere else than logging
        return {"status": 522, "message": "Unprocessable Event"}

    return {"status": 200, "message": "OK"}
