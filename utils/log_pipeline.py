import logging

from utils.db_handler import DBHandler

logger = logging.getLogger('meu_logger_db')
logger.setLevel(logging.DEBUG)

db_handler = DBHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
db_handler.setFormatter(formatter)

logger.addHandler(db_handler)
