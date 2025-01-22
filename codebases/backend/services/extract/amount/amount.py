import re
import logging
from typing import List, Dict, Optional, Tuple
import sys
import os
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging
from backend.utils.extract.filter_text import get_alternative_options
from backend.utils.extract.preprocess_text import filter_empty_lines, filter_lines_without_numbers
from backend.DTO.detail.py.AmountBilledDTO import AmountDetail
from backend.services.extract.invoice_num.invoice_num import COMPANY_PATTERNS
from backend.utils.extract.text_extractor import extract_data_from_text
from backend.utils.extract.preprocess_text import normalize_spaces
setup_logging()

FLEX_SPACE = r'\s{0,2}'

CURRENCY_PATTERN = r'[$€£¥]|USD|EUR|GBP|JPY'
amount_patterns = [
        r"[$€£¥]*\s*([1-9][\d]{0,2}(?:[.,]\d{3})*[.,]\d{2})",  # 0으로 시작하지 않는 금액 패턴
        r"[$€£¥]*\s*([1-9][\d]*[.,]\d{2})"  # 0으로 시작하지 않는 금액 패턴
    ]
exclude_patterns = [
    r'\b\d{4}-\d{2}-\d{2}\b',  # 날짜 형식
    r'\(\d{3}\) \d{3}-\d{4}',  # 전화번호 형식
    r'\b\d{2}:\d{2}\b',        # 시간 형식
    r'\b\d{5}(?:-\d{4})?\b',   # 우편번호 형식
    r'\b\d+%\b',               # 백분율
    r'\b[a-zA-Z]+\b'           # 숫자가 없는 단어
]


def handle_extract_amounts_from_text(text: str, company_code: str) -> Tuple[Optional[Dict], List[Dict]]:
    """
    텍스트에서 청구 금액을 추출하는 함수
    """
    processed_text = filter_empty_lines(text)

    logging.debug(f"handle_extract_amounts_from_text 실행 회사코드: {company_code} ---------------")

    if company_code:
        return extract_with_company_code(processed_text, company_code)
    else:
        return handle_no_company_code(processed_text)


def extract_with_company_code(text: str, company_code: str) -> Tuple[Optional[Dict], List[Dict]]:
    """
    회사 코드가 있는 경우 회사별 패턴으로 금액을 추출하는 함수
    """
    pattern_result = extract_amount_by_company_pattern(text, company_code)
    if pattern_result:
        return [pattern_result], []  # 회사 패턴으로 찾은 경우 대체 옵션 없음
    else:
        return handle_no_company_code(text)


def extract_amount_by_company_pattern(text: str, company_code: str) -> Optional[AmountDetail]:
    """
    회사별 패턴을 사용하여 청구 금액을 추출하는 함수
    """
    if company_code not in COMPANY_PATTERNS:
        logging.debug(f"회사코드 {company_code}가 존재하지 않습니다.")
        return None, []

    pattern = COMPANY_PATTERNS[company_code]['amount']
    logging.debug(f"회사코드 {company_code}의 패턴: {pattern}")

    for keyword in pattern['keywords']:
        extracted_text = extract_data_from_text(
            text=text,
            keyword=keyword,
            extract_type=pattern['extract_type'],
            line_offset=pattern['line_offset']
        )
        if extracted_text:
            logging.debug(f"추출된 데이터: {extracted_text}")
            return match_amount_pattern(extracted_text)

    return None, []


def match_amount_pattern(extracted_text: str) -> Optional[AmountDetail]:
    """
    추출된 텍스트에서 금액 패턴을 매칭하는 함수
    """
    logging.debug(f"match_amount_pattern 실행 추출된 텍스트: {extracted_text}")
    for pattern in amount_patterns:
        amount_match = re.search(pattern, extracted_text)
        logging.debug(f"amount_match: {amount_match}")
        currency_match = re.search(CURRENCY_PATTERN, extracted_text)
        logging.debug(f"currency_match: {currency_match}")

        if amount_match:
            logging.debug(f"매칭된 패턴: {amount_match.group()}")
            logging.debug(f"매칭된 통화: {currency_match.group()}")
            return AmountDetail.from_dict({
                'amount': normalize_spaces(amount_match.group()),
                'currency': currency_match.group() if currency_match else ''
            })

    return AmountDetail.from_dict({'amount': normalize_spaces(extracted_text)})


def handle_no_company_code(text: str) -> Tuple[Optional[AmountDetail], List[AmountDetail]]:
    """
    회사 코드가 없는 경우 금액을 추출하는 함수
    """
    logging.debug("handle_no_company_code 실행")

    candidates = extract_amount_candidates(text)
    
    logging.debug("문맥을 기반으로 금액 후보를 필터링합니다.")
    closest_candidate = filter_amount_candidates_by_context(text, candidates)

    if closest_candidate:
        logging.debug(f"가장 가능성이 높은 금액 후보: {closest_candidate}")
        filtered_candidates = [candidate for candidate in candidates if candidate != closest_candidate]
        return [AmountDetail.from_dict(closest_candidate)], [AmountDetail.from_dict(candidate) for candidate in filtered_candidates]
    else:
        logging.debug("문맥에 맞는 후보가 없으므로, 뒤에서부터 첫 번째 매칭된 결과를 반환합니다.")
        return [AmountDetail.from_dict(candidates[-1])] if candidates else None, [AmountDetail.from_dict(candidate) for candidate in candidates[:-1]] if candidates else []



def extract_amount_candidates(text: str) -> List[Dict]:
    """
    텍스트에서 금액 후보를 추출하는 함수
    """
    logging.debug("텍스트에서 숫자가 없는 줄을 필터링합니다.")
    text_without_numbers = filter_lines_without_numbers(text)
    
    logging.debug("금액 패턴을 정의합니다.")

    logging.debug(f"!!text_without_numbers: {text_without_numbers}")

    candidates = []
    seen_candidates = set()  # 중복 확인을 위한 집합
    for pattern in amount_patterns:
        matches = re.findall(pattern, text_without_numbers)
        for match in matches:
            amount, currency = parse_amount_and_currency(match)
            # 쉼표와 소수점 처리
            normalized_amount = amount.replace('.', '').replace(',', '.')
            try:
                if float(normalized_amount) > 0:
                    candidate = {'amount': amount, 'currency': currency}
                    candidate_tuple = (amount, currency)  # 중복 확인을 위한 튜플
                    if candidate_tuple not in seen_candidates:
                        logging.debug(f"추출된 금액 후보: {amount} {currency}")
                        candidates.append(candidate)
                        seen_candidates.add(candidate_tuple)
            except ValueError:
                logging.error(f"금액 변환 오류: {amount}")

    # 금액을 기준으로 내림차순 정렬
    candidates.sort(key=lambda x: float(x['amount'].replace('.', '').replace(',', '.')), reverse=True)

    return candidates

def filter_amount_candidates_by_context(text: str, candidates: List[Dict]) -> Optional[Dict]:
    """
    문맥을 기반으로 금액 후보를 필터링하여 가장 가능성이 높은 후보를 반환하는 함수
    """
    logging.debug("문맥 키워드를 정의합니다.")
    context_keywords = ["Total", "Amount Due", "Balance"]
    closest_candidate = None
    min_distance = float('inf')

    logging.debug("텍스트를 문장 단위로 나누고, 각 문장에서 금액 후보를 찾습니다.")
    sentences = text.splitlines()
    for sentence in sentences:
        for candidate in candidates:
            candidate_str = candidate['amount']
            candidate_match = re.search(rf"\b{re.escape(candidate_str)}\b", sentence, re.IGNORECASE)
            if candidate_match:
                candidate_pos = candidate_match.start()

                for keyword in context_keywords:
                    keyword_match = re.search(keyword, sentence, re.IGNORECASE)
                    if keyword_match:
                        keyword_pos = keyword_match.start()
                        distance = abs(candidate_pos - keyword_pos)

                        if distance < min_distance:
                            logging.debug(f"가장 가까운 후보 업데이트: {candidate} (거리: {distance})")
                            min_distance = distance
                            closest_candidate = candidate

    return closest_candidate


def parse_amount_and_currency(match: str) -> tuple[str, str]:
    """
    금액과 통화를 분리하는 함수
    """
    # 예시 구현: $123.45 -> ('123.45', 'USD')
    if match.startswith('$'):
        return match[1:], 'USD'
    elif 'USD' in match:
        return match.replace('USD', '').strip(), 'USD'
    return match, ''