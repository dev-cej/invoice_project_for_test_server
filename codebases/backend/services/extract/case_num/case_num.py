import re
import logging
import os
import sys
from typing import Optional, List, Tuple
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging
from backend.utils.pattern.company_patterns import COMPANY_PATTERNS
from backend.utils.extract.preprocess_text import filter_empty_lines, normalize_spaces
from backend.utils.extract.text_extractor import extract_data_from_text


# 로깅 설정 초기화
setup_logging()

def extract_case_numbers_from_text(text):
    """텍스트에서 안건번호를 추출하는 함수"""
    # T는 그대로, M과 D 뒤에는 영문자가 올 수 있게 수정
    pattern = r'\b(?:T|M[A-Z]?|D[A-Z]?)[A-Z0-9-]*\d+[A-Z0-9-]*-[A-Z0-9-]*\b|\b(?:T|M[A-Z]?|D[A-Z]?)[A-Z0-9-]*-[A-Z0-9-]*\d+[A-Z0-9-]*\b'
    matches = re.findall(pattern, text)
    return list(set(matches))

def filter_case_numbers_by_context(text, candidates):
    """문맥을 기반으로 안건번호 후보를 필터링하는 함수"""
    context_keywords = [
        r"Docket\s*No\.?", r"Docket\s*Number", r"Dkt\s*No\.?", r"Dkt\s*Number",
        r"Your\s*Ref\.?", r"Your\s*Reference", r"Your\s*refs", r"Yr\s*Ref", r"Yr\s*Reference",

        r"Ref", r"Reference\s*No\.?", r"Reference\s*Number", r"Ref\s*No\.?", r"Ref\s*Number",
        r"Doc", r"Doc\s*No\.?", r"Doc\s*Number", r"Document\s*No\.?", r"Document\s*Number",
        r"貴社整理番号", r"Y/\s*Ref", r"Y/\s*Reference", r"参照番号", r"案件番号", r"請求書番号", r"注文番号", r"契約番号", r"登録番号"
    ]
    filtered = []
    sentences = text.splitlines()

    candidate_lines = [i for i, sentence in enumerate(sentences) if any(candidate in sentence for candidate in candidates)]

    for i in candidate_lines:
        if any(re.search(keyword, sentences[i]) for keyword in context_keywords):
            candidates_in_sentence = [candidate for candidate in candidates if candidate in sentences[i]]
            filtered.extend(candidates_in_sentence)

    if not filtered:
        filtered.extend(candidates)

    return list(set(filtered))

def extract_case_by_company_pattern(text: str, company_code: str) -> Optional[str]:
    """회사별 패턴을 사용하여 안건번호를 추출하는 함수"""
    if company_code not in COMPANY_PATTERNS:
        return None

    pattern = COMPANY_PATTERNS[company_code]['case_number']

        # 유연한 공백 패턴 (0-2개 공백 허용)

    for keyword in pattern['keywords']:
        extracted_text = extract_data_from_text(
            text=text,
            keyword=keyword,
            extract_type=pattern['extract_type'],
            line_offset=pattern['line_offset']
        )
        
        if extracted_text:
            return normalize_spaces(extracted_text)

    return None

def handle_no_company_code(text: str) -> Tuple[List[str], List[str]]:
    candidates = extract_case_numbers_from_text(text)
    filtered_candidates = filter_case_numbers_by_context(text, candidates)
    return filtered_candidates, []

def extract_case_number_from_text(text: str, company_code: str = None) -> Tuple[List[str], List[str]]:
    """텍스트에서 안건번호를 추출하는 함수"""

    # 텍스트 전처리
    processed_text = filter_empty_lines(text)

    # 1. 회사 코드가 있는 경우 회사별 패턴으로 시도
    if  company_code in ["10101", "10201", "12001"]:
        pattern_result = extract_case_by_company_pattern(processed_text, company_code)
        # 시연용으로 회사코드 10101, 10201 일때만 해당 로직을 적용 (시연용 CASE NUMBER의 패턴이 다르기 때문)
        if company_code in ["10101", "10201", "12001"] and pattern_result:
            return [pattern_result], []  # 회사 패턴으로 찾은 경우 대체 옵션 없음
        else: 
            return handle_no_company_code(processed_text)
    
    else:
        return handle_no_company_code(processed_text)



