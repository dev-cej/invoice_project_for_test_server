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


setup_logging()

def extract_amounts_from_text(text: str) -> List[Dict]:
    """
    텍스트에서 청구 금액을 추출하는 함수
    """
    processed_text = filter_empty_lines(text)

    return handle_no_company_code(processed_text)
   


def extract_amount_candidates(text: str) -> List[Dict]:
    """
    텍스트에서 금액 후보를 추출하는 함수
    """
    logging.debug("텍스트에서 숫자가 없는 줄을 필터링합니다.")
    text_without_numbers = filter_lines_without_numbers(text)
    
    logging.debug("금액 패턴을 정의합니다.")
    amount_patterns = [
        r"[$€£¥]*\s*([\d]{1,3}(?:[.,]\d{3})*[.,]\d{2})",  # 쉼표 또는 소수점이 포함된 금액 패턴
        r"[$€£¥]*\s*([\d]+[.,]\d{2})"  # 소수점 또는 쉼표가 포함된 금액 패턴
    ]

    logging.debug(f"!!text_without_numbers: {text_without_numbers}")

    candidates = []
    for pattern in amount_patterns:
        matches = re.findall(pattern, text_without_numbers)
        for match in matches:
            amount, currency = parse_amount_and_currency(match)
            # 쉼표와 소수점 처리
            normalized_amount = amount.replace('.', '').replace(',', '.')
            try:
                if float(normalized_amount) > 0:
                    logging.debug(f"추출된 금액 후보: {amount} {currency}")
                    candidates.append({'amount': amount, 'currency': currency})
            except ValueError:
                logging.error(f"금액 변환 오류: {amount}")

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

def handle_no_company_code(text: str) -> Tuple[Optional[AmountDetail], List[AmountDetail]]:
    """
    회사 코드가 없는 경우 금액을 추출하는 함수
    """
    logging.debug("금액 후보를 추출합니다.")
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