import logging

logger = logging.getLogger('rgamingtop')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] <%(thread)d> [%(levelname)s] %(message)s', '%d.%m.%Y %H:%M:%S')
file_handler = logging.FileHandler('rgamingtop.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
