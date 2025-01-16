import logging
import re
import os
import sys
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging

setup_logging()

def get_alternative_options(raw_candidates, filtered_candidates):
    """필터링된 후보를 제외한 나머지 후보를 반환하는 함수"""
    logging.debug(f"Raw candidates: {raw_candidates}")
    alternative_options = list(set(raw_candidates) - set(filtered_candidates))
    return alternative_options


    """
    라인에서 키워드를 찾되, 공백과 특수문자의 개수나 위치는 무시
    """
    def clean_text(text: str) -> str:
        # 1단계: 특수문자 주변 공백 제거
        step1 = re.sub(r'\s*([/\-\.])\s*', r'\1', text)
        
        # 2단계: 모든 공백 제거 (split-join 대신 직접 제거)
        step2 = re.sub(r'\s+', '', step1)
        
        # 3단계: 끝의 특수문자 제거
        step3 = step2.rstrip('.:#/：')
        
        # 4단계: 알파벳만 대문자로 (한자는 그대로)
        step4 = ''.join(c.upper() if c.isascii() else c for c in step3)
        
        return step4
    
    # 라인과 키워드 정규화
    clean_line = clean_text(line)
    clean_keyword = clean_text(keyword)
    
    print(f"정규화된 라인: '{clean_line}'")
    print(f"정규화된 키워드: '{clean_keyword}'")
    
    if clean_keyword in clean_line:
        return True, keyword  # 원본 키워드 반환
    
    return False, ""