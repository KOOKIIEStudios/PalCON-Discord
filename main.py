import sys
from socket import timeout

import client
import logger

log = logger.get_logger(__name__)


def get_info():
    try:
        with client.get_client() as con:
            response = con.run("Info")
            log.debug(response)
    except timeout as e:
        log.error("Unable to fetch server info!\n", e)


if __name__ == "__main__":
    get_info()
    
    logger.shutdown_logger()
    sys.exit(0)
