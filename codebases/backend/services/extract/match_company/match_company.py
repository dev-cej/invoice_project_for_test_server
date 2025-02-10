from fuzzywuzzy import fuzz # 문자열 유사도 계산을 위한 라이브러리
import logging
from config.logging_config import setup_logging
from utils.extract.preprocess_text import preprocess_text, preprocess_line
setup_logging()

def calculate_similarity(processed_line, company, threshold):
    """회사 이름과 줄의 유사도를 계산하는 함수"""
    processed_short_name = preprocess_text(company['short_name'])  # 회사의 짧은 이름 전처리
    processed_name = preprocess_text(company['name'])  # 회사의 전체 이름 전처리
    
    # 최소 길이 조건 추가
    if len(processed_line) < 3:  # 줄의 길이가 3 미만이면 None 반환
        return None
    
    # 유사도 계산
    ratio_short_name = fuzz.partial_ratio(processed_line, processed_short_name)  # 짧은 이름과의 유사도 계산
    ratio_name = fuzz.partial_ratio(processed_line, processed_name)  # 전체 이름과의 유사도 계산
    
    # 유사도가 임계값 이상인 경우 결과 반환
    if ratio_name >= threshold or ratio_short_name >= threshold:  # 유사도가 임계값 이상이면
        return {
            'phrase': processed_line,  # 원본 구문
            'company': company,  # 회사 정보
            'similarity': max(ratio_short_name, ratio_name),  # 최대 유사도
            'preferred': 'name' if ratio_name >= ratio_short_name else 'short_name'  # 선호하는 매칭 타입
        }
    return None  # 임계값 미만이면 None 반환

def process_lines(lines, companies, threshold, start, end):
    """주어진 범위의 줄을 처리하여 유사한 구문을 찾는 함수"""
    similar_phrases = []  # 유사 구문 저장 리스트
    for i in range(start, end):  # 지정된 범위의 줄을 순회
        line = preprocess_line(lines[i])  # 줄 전처리
        processed_line = preprocess_text(line)  # 전처리된 줄
        for company in companies:  # 각 회사에 대해
            similarity_result = calculate_similarity(processed_line, company, threshold)  # 유사도 계산
            if similarity_result:  # 유사도가 임계값 이상이면
                similarity_result['phrase'] = line  # 원본 구문 저장
                similar_phrases.append(similarity_result)  # 유사 구문 리스트에 추가
                if similarity_result['similarity'] >= 90 and similarity_result['preferred'] == 'name':  # 높은 유사도 조기 종료 조건
                    return similar_phrases  # 유사 구문 반환
    return similar_phrases  # 유사 구문 반환

def find_similar_phrases_in_text(text, companies, threshold=90):
    """텍스트에서 회사 이름과 유사한 구문을 찾는 함수"""
    similar_phrases = []  # 유사 구문 저장 리스트
    try:
        lines = text.splitlines()  # 텍스트를 줄 단위로 분할
        num_lines = len(lines)  # 줄 수 계산
        
        similar_phrases.extend(process_lines(lines, companies, threshold, 0, min(5, num_lines)))  # 처음 5줄 처리
        similar_phrases.extend(process_lines(lines, companies, threshold, max(0, num_lines - 5), num_lines))  # 마지막 5줄 처리

        if not similar_phrases:  # 유사 구문이 없으면
            similar_phrases.extend(process_lines(lines, companies, threshold, 5, num_lines - 5))  # 중간 줄 처리

    except Exception as e:  # 예외 발생 시
        logging.error(f"유사 구문 찾기 오류: {str(e)}", exc_info=True)  # 에러 로그 기록
    return similar_phrases  # 유사 구문 반환


def select_matched_candidate(similar_phrases):
    """가장 많이 일치하는 code를 가진 후보자 중에서 일치율이 가장 높은 것을 선택"""
    if not similar_phrases:  # 유사 구문이 없으면
        return None, []  # None과 빈 리스트 반환

    code_groups = {}  # 코드별 그룹화 딕셔너리
    for phrase in similar_phrases:  # 각 유사 구문에 대해
        code = phrase['company']['code']  # 회사 코드 추출
        if code not in code_groups:  # 코드가 그룹에 없으면
            code_groups[code] = []  # 새로운 리스트 생성
        code_groups[code].append(phrase)  # 구문 추가

    max_code_group = max(code_groups.values(), key=len)  # 가장 많은 구문을 가진 그룹 선택

    matched_candidate = max(max_code_group, key=lambda x: x['similarity'])  # 최고 유사도 구문 선택

    alternative_options = [phrase for phrase in max_code_group if phrase != matched_candidate]  # 대체 옵션 생성

    return matched_candidate, alternative_options  # 선택된 후보와 대체 옵션 반환