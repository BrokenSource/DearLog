import random
import time

from dearlog import logger

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
    time.sleep(random.uniform(0.1, 0.3))

