import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.warning("Nothing to do")
    
    return {"status": 200, "message": "OK"}

