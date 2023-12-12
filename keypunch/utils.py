import os
import logging

fmt = "%(levelname)s:%(asctime).19s: %(message)s"
logging.basicConfig(format=fmt)
logger = logging.getLogger("javelin")
if os.environ.get("KEYPUNCH_DEBUG"):
    logger.setLevel("DEBUG")
    logger.debug("Log level set to debug")
