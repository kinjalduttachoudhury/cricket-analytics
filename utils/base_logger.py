import logging

logger = logging

logger.basicConfig(
    filename="output.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
    force=True
)