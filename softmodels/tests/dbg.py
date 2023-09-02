# setup_logger.py
import logging
FORMAT = '[%(filename)s:%(lineno)s - %(funcName)12s()][%(levelname)s]  %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('dbg')