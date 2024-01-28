import sys

import client
import logger

log = logger.get_logger(__name__)
#
#
# Initial implementation
# def test_get_info():
#     try:
#         with client.get_client() as con:
#             response = con.run("Info")
#             log.debug(response)
#     except timeout as e:
#         log.error("Unable to fetch server info!\n", e)


def fallback_get_info():
    client.send_command_fallback("Info")


if __name__ == "__main__":
    test_fetch_config = client.fetch_config()
    if not test_fetch_config:
        logger.shutdown_logger()
        sys.exit(0)

    fallback_get_info()
    
    logger.shutdown_logger()
    sys.exit(0)
