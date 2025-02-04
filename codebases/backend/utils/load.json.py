import json
import logging
import os
import sys
from config.logging_config import setup_logging

setup_logging()

def load_json_file(file_path):
    """JSON 파일을 로드하는 함수"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logging.error("파일을 찾을 수 없습니다.", exc_info=True)
        return {'status': 'error', 'message': '파일을 찾을 수 없습니다.'}
    except json.JSONDecodeError:
        logging.error("JSON 디코딩 오류가 발생했습니다.", exc_info=True)
        return {'status': 'error', 'message': 'JSON 디코딩 오류가 발생했습니다.'}
    except Exception as e:
        logging.error(f"오류 발생: {str(e)}", exc_info=True)
        return {'status': 'error', 'message': f'오류 발생: {str(e)}'}