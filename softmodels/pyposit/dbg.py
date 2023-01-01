# setup_logger.py
import logging
FORMAT = '[%(name)s:%(levelname)s]  %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('dbg')