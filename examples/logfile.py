from pathlib import Path

from dearlog import FileHandler, logger

# Add file handler to logger
logger.handlers.append(FileHandler(
    path=Path(__file__).parent/"logfile.txt",
    mode="a", # "w" to overwrite each run
))

def fizzbuzz(n: int) -> str:
    return ("Fizz"*(n%3==0) + "Buzz"*(n%5==0)) or str(n)

logger.info("Start program")

for n in range(1, 101):
    logger.minor(fizzbuzz(n))

logger.ok("Finished program")
