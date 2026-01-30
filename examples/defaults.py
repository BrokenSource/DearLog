from dearlog import logger

logger.info("I am this fast to import!")
logger.info("without rich, that is..")

import random
import time

while True:
    method = random.choice((
        logger.info,
        logger.note,
        logger.ok,
        logger.minor,
        logger.skip,
        logger.todo,
        logger.tip,
        logger.fixme,
        logger.warn,
        logger.error,
        logger.crit
    ))

    method("Hello, DearLog!")
    time.sleep(random.uniform(0.0, 0.3))

