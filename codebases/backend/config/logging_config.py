import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_directory = '/var/www/html/invoiceProject/logs'
    log_file = 'python_script.log'
    log_path = os.path.join(log_directory, log_file)

    # 로그 디렉토리가 없으면 생성
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    handler = RotatingFileHandler(log_path, maxBytes=1*1024*1024, backupCount=1)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    if not logger.hasHandlers():
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    logging.getLogger('pdfminer').setLevel(logging.WARNING)

    # fuzzywuzzy 로거의 로그 레벨을 조정
    logging.getLogger('fuzzywuzzy').setLevel(logging.ERROR)
