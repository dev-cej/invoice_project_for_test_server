import re
import logging
import os
import sys
from config.logging_config import setup_logging

# 로깅 설정 초기화
setup_logging()

def preprocess_text(text):
    """텍스트 전처리 함수: 대소문자 변환 및 공백 제거"""
    try:
        processed_text = re.sub(r'\s+', '', text).lower()
        return processed_text
    except Exception as e:
        logging.error(f"텍스트 전처리 오류: {str(e)}", exc_info=True)
        return ''

def preprocess_line(line):
    """특정 패턴을 제거하여 전처리된 줄을 반환"""
    # 콜론을 기준으로 문장 분리
    if ':' in line:
        return line.split(':', 1)[1].strip()
    return line.strip()


def filter_lines_without_numbers(text: str) -> str:

    if not text:
        return ""
        
    processed_lines = [
        line for line in text.splitlines()
        if any(c.isdigit() for c in line)
    ]
    return '\n'.join(processed_lines)


def filter_empty_lines(text: str) -> str:

    if not text:
        return ""
        
    return '\n'.join(
        line for line in text.splitlines()
        if line.strip()  # 공백만 있는 라인도 제거
    )

def normalize_spaces(text: str) -> str:
    """
    텍스트의 공백을 정규화하는 함수
    - 앞뒤 공백 제거
    - 연속된 공백을 하나로 통일
    """
    if not text:
        return ""
    text = text.strip()
    return re.sub(r'\s+', ' ', text)