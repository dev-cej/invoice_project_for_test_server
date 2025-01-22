import re
import logging
import os
import sys
from typing import Optional, List, Tuple
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging
from backend.utils.extract.filter_text import get_alternative_options
from backend.services.extract.case_num.case_num import extract_case_numbers_from_text
from backend.utils.extract.text_extractor import extract_data_from_text
from backend.utils.pattern.company_patterns import COMPANY_PATTERNS
from backend.utils.extract.preprocess_text import filter_lines_without_numbers, filter_empty_lines

setup_logging()

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

def get_invoice_patterns(flex_space: str) -> List[str]:
    """
    송장 번호 패턴 목록을 반환하는 함수
    Args:
        flex_space: 유연한 공백을 위한 정규식 패턴
    """
    return [
        rf'\b\d{{4}}{flex_space}-{flex_space}\d{{5,6}}\b',              # 2024-XXXXX
        rf'\b[A-Z]+{flex_space}-{flex_space}24{flex_space}-{flex_space}\d{{5,6}}\b',          # PA-24-XXXXX
        rf'\b\d+{flex_space}-{flex_space}\d+{flex_space}-{flex_space}24{flex_space}\.{flex_space}\d+\b',  # XX-XXX-24.XXXXX
        rf'\bPTDN{flex_space}\d+{flex_space}/{flex_space}\d{{4}}\b',    # PTDN/2024
        rf'\b[A-Z]{{2,3}}{flex_space}24{flex_space}\d+\b',              # XX24XXXXX
        r'\b\d{6,}\b',                                                   # 6자리 이상 숫자
        rf'\b[A-Z0-9]{flex_space}[-]{{0,1}}{flex_space}[A-Z0-9-]{{4,}}\b'  # 일반적인 영숫자 조합
    ]

def get_exclude_patterns(flex_space: str) -> List[str]:
    """
    제외할 패턴 목록을 반환하는 함수
    Args:
        flex_space: 유연한 공백을 위한 정규식 패턴
    """
    return [
        # 날짜 형식 (공백 허용)
        rf'^(\d{{4}}{flex_space}[-/]{flex_space}\d{{1,2}}{flex_space}[-/]{flex_space}\d{{1,2}}|\d{{1,2}}{flex_space}[-/]{flex_space}\d{{1,2}}{flex_space}[-/]{flex_space}\d{{4}})$',
        # 숫자가 없는 단어들
        r'^[A-Za-z\s]+$'
    ]

def extract_invoice_candidates(text):
    """텍스트에서 송장 번호 후보를 탐지하는 함수"""
    patterns = [
        # 2024년 관련 패턴
        r'\b(\d{4}-\d{5,6})\b',              # 2024-XXXXX
        r'\b([A-Z]+-24-\d{5,6})\b',          # PA-24-XXXXX
        r'\b(\d{4}/\d{1,2}/\d{1,4})\b',      # 2024/XX/XXXX
        
        # 특수 형식 패턴
        r'\b(\d+-\d+-24\.\d+)\b',            # XX-XXX-24.XXXXX
        r'\b(PTDN\d+/\d{4})\b',              # PTDN/2024
        
        # 알파벳+숫자 조합 패턴
        r'\b(QKD24\d+)\b',                   # QKD24XXXXXX
        r'\b(JD240\d+)\b',                   # JD240XXXX
        r'\b(PAF240\d+)\b',                  # PAF240XXXXX
        r'\b(T24BJ\d+)\b',                   # T24BJXXXXXX
        r'\b(AF2024\d+)\b',                  # AF2024XXXXX
        
        # 추가적인 특수 패턴들
        r'\b([A-Z]{2,3}24\d+)\b',            # XX24XXXXX
        r'\b(\d{2}-\d{3}-24\.\d+)\b',        # XX-XXX-24.XXXXX
        
        # 일반 숫자 패턴
        r'\b(\d{6,})\b',                     # 6자리 이상 숫자
    ]
    
    candidates = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        candidates.extend(matches)

    # case_num 추출
    case_nums = extract_case_numbers_from_text(text)

    # case_num을 후보에서 제외
    filtered_candidates = [candidate for candidate in candidates if candidate not in case_nums]

    
    return list(set(filtered_candidates))

def filter_candidates_by_context(text, candidates):
    """문맥을 기반으로 송장 번호 후보를 필터링하는 함수"""
    # 공백 패턴 정의
    SPACE = r"[ ]{0,2}"  # 최대 2개까지의 공백만 허용
    DOT = r"\.?"         # 선택적 마침표
    
    context_keywords = [
        # 기본 형식
        fr"Invoice{SPACE}N[oº]{DOT}",      # "Invoice No", "Invoice  No."
        fr"Invoice{SPACE}Number",           # "Invoice Number"
        fr"D/N{SPACE}NO{DOT}",             # "D/N NO", "D/N  NO."
        fr"Debit{SPACE}Note{SPACE}N[oº]{DOT}",  # "Debit Note No"
        
        # 특수 형식
        fr"Tax{SPACE}Invoice{SPACE}No{DOT}",   # "Tax Invoice No"
        fr"INVOICE{SPACE}Nº",                  # "INVOICE Nº"
        r"請求No",                             # 일본어는 공백 없음
        fr"NO{DOT}{SPACE}UP",                 # "NO UP", "NO.  UP"
        
        # 간단한 형식
        fr"NO{DOT}",                          # "NO", "NO."
        fr"Inv{SPACE}No{DOT}",                # "Inv No", "Inv  No."
        fr"DN{SPACE}No{DOT}",                 # "DN No", "DN  No."
        
        # 기타 형식
        fr"Bill{SPACE}No{DOT}",               # "Bill No", "Bill  No."
        fr"Billing{SPACE}Code",               # "Billing Code"
        fr"Receipt{SPACE}No{DOT}",            # "Receipt No"
        fr"Transaction{SPACE}ID",             # "Transaction ID"
        fr"Payment{SPACE}Ref",                # "Payment Ref"
    ]
    filtered = []
    sentences = text.splitlines()  # 텍스트를 문장 단위로 나눔

    for sentence in sentences:
        closest_candidate = None
        min_distance = float('inf')

        for candidate in candidates:
            # 문맥 키워드와 후보의 위치를 찾음
            candidate_match = re.search(rf"\b{re.escape(candidate)}\b", sentence)
            if candidate_match:
                candidate_pos = candidate_match.start()

                for keyword in context_keywords:
                    keyword_match = re.search(keyword, sentence)
                    if keyword_match:
                        keyword_pos = keyword_match.start()
                        distance = abs(candidate_pos - keyword_pos)

                        # 가장 가까운 후보를 선택
                        if distance < min_distance:
                            min_distance = distance
                            closest_candidate = candidate

        if closest_candidate:
            filtered.append(closest_candidate)

    return list(set(filtered))

def extract_invoice_by_company_pattern(text: str, company_code: str) -> Optional[str]:
    """
    회사별 패턴을 사용하여 송장 번호를 추출하는 함수
    
    Args:
        text: 전체 텍스트
        company_code: 회사 코드
    
    Returns:
        추출된 송장 번호 또는 None
    """
    if company_code not in COMPANY_PATTERNS:
        return None
        
    pattern = COMPANY_PATTERNS[company_code]['invoice_number']

    # 유연한 공백 패턴 (0-2개 공백 허용)
    FLEX_SPACE = r'\s{0,2}'
    
    # 패턴 목록 가져오기
    invoice_patterns = get_invoice_patterns(FLEX_SPACE)
    exclude_patterns = get_exclude_patterns(FLEX_SPACE)

    for keyword in pattern['keywords']:
        extracted_text = extract_data_from_text(
            text=text,
            keyword=keyword,
            extract_type=pattern['extract_type'],
            line_offset=pattern['line_offset']
        )
        
        # 추출된 데이터가 단어가 아닌 구문인 경우 처리
        # 1개의 단어가 문장으로 추출되는 경우
        if extracted_text:
            # 공백 3개 이상으로 분리
            parts = re.split(r'\s{3,}', extracted_text)
            
            # 분리된 부분이 있는 경우에만 패턴 매칭 진행
            if len(parts) > 1:
                for part in parts:
                    part = normalize_spaces(part)
                    
                    # 너무 짧은 텍스트 제외
                    if len(part.replace(' ', '')) < 5:
                        continue
                    
                    # 제외 패턴 확인
                    if any(re.match(exclude_pattern, part) for exclude_pattern in exclude_patterns):
                        continue
                    
                    # 송장 번호 패턴 매칭
                    for invoice_pattern in invoice_patterns:
                        match = re.search(invoice_pattern, part)
                        if match:
                            return normalize_spaces(match.group())
            
            # 분리되지 않았거나 패턴 매칭 실패시 원본 반환
            return normalize_spaces(extracted_text)

    return None

def handle_no_company_code(text: str) -> Tuple[List[str], List[str]]:
    candidates = extract_invoice_candidates(text)
    filtered_candidates = filter_candidates_by_context(text, candidates)
    alternative_options = get_alternative_options(candidates, filtered_candidates)
    return filtered_candidates, alternative_options

def extract_invoice_number_from_text(text: str, company_code: str = None) -> Tuple[List[str], List[str]]:
    """텍스트에서 송장 번호를 추출하는 함수"""

    # 텍스트 전처리
    processed_text = filter_empty_lines(text)  # 빈 라인 제거도 포함되어 있음


    # 1. 회사 코드가 있는 경우 회사별 패턴으로 시도
    if company_code:
        pattern_result = extract_invoice_by_company_pattern(processed_text, company_code)
        if pattern_result:
            return [pattern_result], []  # 회사 패턴으로 찾은 경우 대체 옵션 없음
        else: 
            return handle_no_company_code(processed_text)
    
    else:
        return handle_no_company_code(processed_text)



