import sys
import logging


def configure_logging(namespace):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO if not namespace.debug else logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' if namespace.verbose else '%(message)s'
    sh.setFormatter(logging.Formatter(formatter))
    logger.addHandler(sh)
    return logger
