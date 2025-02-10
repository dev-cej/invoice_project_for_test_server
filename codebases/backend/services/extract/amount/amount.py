import re
import logging
from typing import List, Dict, Optional, Tuple
import sys
import os
from config.logging_config import setup_logging
from utils.extract.preprocess_text import filter_empty_lines, filter_lines_without_numbers
from DTO.detail.py.AmountBilledDTO import AmountDetail


setup_logging()

amount_patterns = [
    r"\b[$€£¥]?\s*([1-9]\d{0,2}(?:,\d{3})*\.\d{2})\b",  # 쉼표로 천 단위 구분, 점으로 소수점
    r"\b[$€£¥]?\s*([1-9]\d{0,2}(?:\.\d{3})*,\d{2})\b"  # 점으로 천 단위 구분, 쉼표로 소수점
]

context_keywords = ["TOTAL AMOUNT DUE", "Total", "Amount Due", ]
currency_symbols = ["$", "€", "£", "¥", "USD", "EUR", "GBP", "JPY"]  # 통화 기호 및 코드 추가

def extract_amounts_from_text(text: str) -> List[Dict]:
    """
    텍스트에서 청구 금액을 추출하는 함수
    """
    processed_text = filter_empty_lines(text)
    processed_text = filter_lines_without_numbers(processed_text)

    return handle_no_company_code(processed_text)
   


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
    logging.debug("문맥을 기반으로 금액 후보를 필터링합니다.")
    
    # candidates가 비어있는 경우 처리
    if not candidates:
        return None
        
    closest_candidate = None
    best_score = float('inf')

    # 거리와 금액 크기에 대한 가중치 설정
    distance_weight = 0.7
    amount_weight = 0.2
    position_weight = 0.1  # 후보의 위치에 대한 가중치 추가

    # 금액 후보들에서 최대 금액을 찾기
    max_amount = max(float(candidate['amount'].replace(',', '').replace('.', '')) for candidate in candidates)

    for index, candidate in enumerate(candidates):
        candidate_str = candidate['amount']
        candidate_match = re.search(rf"\b{re.escape(candidate_str)}\b", text, re.IGNORECASE)
        if candidate_match:
            candidate_pos = candidate_match.start()  # 후보 금액의 시작 위치

            # 문맥 키워드와의 거리 계산
            min_keyword_distance = float('inf')  # 문맥 키워드와의 최소 거리 초기화
            for keyword in context_keywords:
                if keyword in text:  # 문맥 키워드가 텍스트에 존재하는지 확인
                    keyword_match = re.search(keyword, text, re.IGNORECASE)
                    if keyword_match:
                        keyword_pos = keyword_match.start()  # 문맥 키워드의 시작 위치
                        distance = abs(candidate_pos - keyword_pos)  # 거리 계산
                        logging.debug(f"문맥 키워드 '{keyword}'와의 거리: {distance}")
                        if distance < min_keyword_distance:
                            min_keyword_distance = distance  # 최소 거리 업데이트

            # 유효한 거리만 고려
            if min_keyword_distance == float('inf'):
                continue  # 통화 기호와 문맥 키워드가 모두 없으면 후보 무시

            # 두 거리의 합을 계산
            combined_distance = min_keyword_distance
            logging.debug(f"후보 '{candidate_str}'의 통화 및 문맥 거리 합: {combined_distance}")

            # 금액 크기 비교
            normalized_amount = float(candidate_str.replace(',', '').replace('.', ''))

            # 거리와 금액 크기를 정규화하여 점수 계산
            normalized_distance = combined_distance / (combined_distance + 1)  # 거리 정규화
            normalized_amount_score = normalized_amount / max_amount  # 금액 정규화

            # 후보의 위치에 따른 점수 조정
            position_score = index / len(candidates)  # 후보의 위치를 정규화
            score = (distance_weight * normalized_distance) - (amount_weight * normalized_amount_score) + (position_weight * position_score)
            logging.debug(f"후보 '{candidate_str}'의 점수: {score}")

            if score < best_score:
                logging.debug(f"가장 가까운 후보 업데이트: {candidate} (점수: {score})")
                best_score = score  # 최적의 점수 업데이트
                closest_candidate = candidate  # 가장 가까운 후보 업데이트

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