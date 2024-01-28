import sys

import logger


log = logger.get_logger(__name__)


if __name__ == "__main__":
    log.info("Hello world!")
    
    logger.shutdown_logger()
    sys.exit(0)
