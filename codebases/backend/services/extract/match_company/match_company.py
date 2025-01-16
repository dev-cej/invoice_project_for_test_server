from fuzzywuzzy import fuzz
import logging
import os
import sys
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging
from backend.utils.extract.preprocess_text import preprocess_text, preprocess_line
setup_logging()

def calculate_similarity(processed_line, company, threshold):
    """회사 이름과 줄의 유사도를 계산하는 함수"""
    processed_short_name = preprocess_text(company['short_name'])
    processed_name = preprocess_text(company['name'])
    
    # 최소 길이 조건 추가
    if len(processed_line) < 3:
        return None
    
    # 유사도 계산
    ratio_short_name = fuzz.partial_ratio(processed_line, processed_short_name)
    ratio_name = fuzz.partial_ratio(processed_line, processed_name)
    
    # 유사도가 임계값 이상인 경우 결과 반환
    if ratio_name >= threshold or ratio_short_name >= threshold:
        return {
            'phrase': processed_line,
            'company': company,
            # 두 유사도 중 더 높은 값을 유사도로 설정
            'similarity': max(ratio_short_name, ratio_name),
            # 더 높은 유사도를 가진 회사 이름을 선호하는 것으로 설정
            'preferred': 'name' if ratio_name >= ratio_short_name else 'short_name'
        }
    return None

def process_lines(lines, companies, threshold, start, end):
    """주어진 범위의 줄을 처리하여 유사한 구문을 찾는 함수"""
    similar_phrases = []
    for i in range(start, end):
        line = preprocess_line(lines[i])
        processed_line = preprocess_text(line)
        # logging.debug(f"처리된 줄: {processed_line}")
        for company in companies:
            similarity_result = calculate_similarity(processed_line, company, threshold)
            if similarity_result:
                # 원래 텍스트 형태로 phrase 저장
                similarity_result['phrase'] = line
                similar_phrases.append(similarity_result)
                # 높은 유사도를 가진 결과를 조기에 반환하여 성능을 최적화
                # 전체 이름이 더 신뢰할 수 있는 매칭을 제공한다고 판단될 때 조기 종료
                if similarity_result['similarity'] >= 90 and similarity_result['preferred'] == 'name':
                    # logging.debug("높은 유사도 발견, 검색 중단")
                    return similar_phrases
    return similar_phrases

def find_similar_phrases_in_text(text, companies, threshold=90):
    """텍스트에서 회사 이름과 유사한 구문을 찾는 함수"""
    # logging.debug("find_similar_phrases_in_text 시작!")
    similar_phrases = []
    try:
        lines = text.splitlines()
        num_lines = len(lines)

        similar_phrases.extend(process_lines(lines, companies, threshold, 0, min(5, num_lines)))
        similar_phrases.extend(process_lines(lines, companies, threshold, max(0, num_lines - 5), num_lines))

        if not similar_phrases:
            similar_phrases.extend(process_lines(lines, companies, threshold, 5, num_lines - 5))

        # logging.debug("유사 구문 찾기 성공")
    except Exception as e:
        logging.error(f"유사 구문 찾기 오류: {str(e)}", exc_info=True)
    return similar_phrases


def select_matched_candidate(similar_phrases):
    """가장 많이 일치하는 code를 가진 후보자 중에서 일치율이 가장 높은 것을 선택"""
    # logging.debug(f"select_matched_candidate 시작: {similar_phrases}")
    if not similar_phrases:
        return None, []

    code_groups = {}
    for phrase in similar_phrases:
        code = phrase['company']['code']
        if code not in code_groups:
            code_groups[code] = []
        code_groups[code].append(phrase)

    max_code_group = max(code_groups.values(), key=len)

    matched_candidate = max(max_code_group, key=lambda x: x['similarity'])

    alternative_options = [phrase for phrase in max_code_group if phrase != matched_candidate]

    return matched_candidate, alternative_options