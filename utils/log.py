import logging
from systemd.journal import JournalHandler

level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.addHandler(JournalHandler())
logger.setLevel(level)
