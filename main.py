import asyncio
import sys

import client
import logger

log = logger.get_logger(__name__)


async def test_async_connection():  # for testing purposes only
    server = client.AsyncClient()  # init using config files
    log.debug(await server.info())
    log.debug(await server.online())


async def test_connection():  # proof of concept
    server = client.Client()
    log.debug(server.info())
    log.debug(server.online())


if __name__ == "__main__":
    test_fetch_config = client.fetch_config()
    if not test_fetch_config:
        logger.shutdown_logger()
        sys.exit(0)

    # REMOVE THIS AFTER TESTING:
    asyncio.run(test_connection())
    
    logger.shutdown_logger()
    sys.exit(0)
