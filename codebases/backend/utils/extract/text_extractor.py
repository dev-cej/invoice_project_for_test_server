# text_extractor.py
import re
import logging
from backend.config.logging_config import setup_logging
from typing import Tuple, List

setup_logging()

def clean_text(text: str) -> str:
    """
    텍스트 정규화 함수
    
    Args:
        text: 정규화할 텍스트
    
    Returns:
        정규화된 텍스트
        
    정규화 과정:
        1. 특수문자(/, -, .) 주변의 공백 제거
        2. 연속된 공백을 하나로 변환
        3. 끝의 특수문자(.:#/：) 제거
        4. 알파벳을 대문자로 변환 (한자는 유지)
    """
    # 1단계: 특수문자 주변 공백 제거
    # 예: "D / N" -> "D/N"
    step1 = re.sub(r'\s*([/\-\.])\s*', r'\1', text)
    
    # 2단계: 연속된 공백을 하나로
    # 예: "D/N    No" -> "D/N No"
    step2 = re.sub(r'\s+', ' ', step1)
    
    # 3단계: 끝의 특수문자 제거
    # 예: "D/N No." -> "D/N No"
    step3 = step2.rstrip('.:#/：')
    
    # 4단계: 알파벳만 대문자로 (한자는 그대로)
    # 예: "Invoice No" -> "INVOICE NO"
    return ''.join(c.upper() if c.isascii() else c for c in step3)

def find_keyword_in_line(line: str, keyword: str) -> Tuple[bool, str]:
    """
    라인에서 키워드를 찾는 함수
    
    Args:
        line: 검색할 라인
        keyword: 찾을 키워드
    
    Returns:
        (찾았는지 여부, 매칭된 원본 키워드)
    """
    # 1. 먼저 clean_text로 전처리
    clean_line = clean_text(line)
    clean_keyword = clean_text(keyword)
    
    # 2. 전처리된 텍스트를 단어 단위로 분리
    words = re.split(r'[\s:\.：]+', clean_line)
    keyword_parts = re.split(r'[\s:\.：]+', clean_keyword)
    
    # 분리된 단어들 중에서 빈 문자열을 제거
    words = [w for w in words if w]
    keyword_parts = [w for w in keyword_parts if w]
    
    
    # 3. 단일 키워드인 경우 (예: "No")
    if len(keyword_parts) == 1:
        found = keyword_parts[0] in words
        logging.debug(f"!!find_keyword_in_line 단일 키워드 매칭 시작: {keyword_parts} \n word: {words}")
        if found:
            logging.debug(f"!!find_keyword_in_line 단일 키워드 매칭 성공: {keyword}")
        return found, keyword
    
    # 4. 여러 단어로 된 키워드인 경우 (예: "Invoice No")
    for i in range(len(words) - len(keyword_parts) + 1):
        logging.debug(f"!!find_keyword_in_line 복합 키워드 매칭 시작: {keyword_parts} \n word: {words}")
        if words[i:i+len(keyword_parts)] == keyword_parts:
            logging.debug(f"!!find_keyword_in_line 복합 키워드 매칭 성공: {keyword}")
            return True, keyword
            
    return False, ""

def remove_text_after_multiple_spaces(text: str, space_count: int = 3) -> str:
    """
    연속된 공백 이후의 텍스트를 제거하는 함수
    
    Args:
        text: 처리할 텍스트
        space_count: 기준이 되는 연속 공백 개수 (기본값: 3)
    
    Returns:
        공백 처리된 텍스트
    
    Examples:
        >>> remove_text_after_multiple_spaces("QKD241125023   추가텍스트")
        "QKD241125023"
        >>> remove_text_after_multiple_spaces("QKD 241125023")
        "QKD 241125023"
    """
    parts = re.split(rf'\s{{{space_count},}}', text)
    return parts[0].strip()

def extract_after_separator(text: str, separators: List[str]) -> str:
    """
    구분자 이후의 텍스트를 추출하는 함수
    
    Args:
        text: 처리할 텍스트
        separators: 구분자 목록 (예: [':', '：', '.', '-'])
    
    Returns:
        구분자 이후의 텍스트 (구분자가 없는 경우 원본 텍스트)
    
    Examples:
        >>> extract_after_separator(".: QKD241125023", [':', '.'])
        "QKD241125023"
        >>> extract_after_separator("QKD241125023", [':'])
        "QKD241125023"
    """
    # 구분자들을 정규식 패턴으로 변환
    separator_pattern = '[' + re.escape(''.join(separators)) + ']'
    # 구분자 주변 공백과 연속된 구분자를 하나로 처리
    normalized_text = re.sub(rf'\s*({separator_pattern}+)\s*', r'\1', text)
    logging.debug(f"!!extract_after_separator 정규화된 텍스트: {normalized_text}")
    
    # 연속된 구분자들의 마지막 위치 찾기
    match = re.match(rf'^[\s]*({separator_pattern}+)', normalized_text)
    if match:
        # 구분자 이후의 텍스트 추출
        return normalized_text[match.end():].strip()
    
    return normalized_text.strip()

def extract_after_keyword(line: str, keyword: str, separators: List[str]) -> str:
    """
    키워드 뒤의 데이터를 추출하는 함수
    
    Args:
        line: 검색할 라인
        keyword: 찾을 키워드
        separators: 구분자 목록 (예: [':', '：', '.', '-'])
    
    Returns:
        추출된 데이터 (못 찾은 경우 빈 문자열)
    
    처리 순서:
        1. 키워드 위치 찾기 (대소문자 구분 없음)
        2. 키워드 다음 텍스트에서 구분자 처리
        3. 구분자 이후 텍스트 추출
        4. 3개 이상 연속된 공백 이후 텍스트 제거
    """
    logging.debug(f"!!extract_after_keyword 시작: line: {line} keyword: {keyword} separators: {separators}")

    # 1. 키워드 위치 찾기 (대소문자 구분 없이)
    keyword_pos = line.lower().find(keyword.lower())
    if keyword_pos == -1:  # 키워드를 찾지 못한 경우
        return ""
    
    # 2. 키워드 다음 텍스트 추출
    keyword_end = keyword_pos + len(keyword)
    remaining_text = line[keyword_end:]
    
    # 3. 구분자 처리 및 텍스트 추출
    extracted_text = extract_after_separator(remaining_text, separators)
    logging.debug(f"!!extract_after_keyword 추출된 텍스트: {extracted_text}")

    # 4. 3개 이상 연속된 공백 이후 텍스트 제거
    result = remove_text_after_multiple_spaces(extracted_text)
    logging.debug(f"!!extract_after_keyword 최종 추출 결과: {result}")
    return result

def extract_data_from_text(
    text: str, 
    keyword: str, 
    extract_type: str = 'after_keyword',
    line_offset: int = 0,
    separators: List[str] = [':', '：', '.', '-', '#']
) -> str:
    """
    텍스트에서 키워드를 찾고 데이터를 추출하는 메인 함수
    
    Args:
        text: 검색할 전체 텍스트
        keyword: 찾을 키워드
        extract_type: 추출 방식
            - 'after_keyword': 키워드 뒤의 데이터만 추출 (기본값)
            - 'line': 라인 전체를 추출
        line_offset: 키워드가 있는 라인 기준 상대적 위치
            - 0: 같은 줄 (기본값)
            - 1: 다음 줄
            - -1: 이전 줄
        separators: 구분자 목록 (기본값: [':', '：', '.', '-', '=', '>'])
    
    Returns:
        추출된 데이터 (못 찾은 경우 빈 문자열)
    
    Examples:
        >>> text = '''
        Invoice Details
        Invoice No: ABC123
        Date: 2024-01-01
        '''
        
        # 1. 키워드 뒤 데이터 추출
        >>> extract_data_from_text(text, "Invoice No")
        'ABC123'
        
        # 2. 라인 전체 추출
        >>> extract_data_from_text(text, "Invoice No", "line")
        'Invoice No: ABC123'
        
        # 3. 다음 줄 추출
        >>> extract_data_from_text(text, "Invoice No", line_offset=1)
        'Date: 2024-01-01'
    
    처리 과정:
        1. 텍스트를 라인 단위로 분리
        2. 각 라인에서 키워드 검색
        3. 키워드를 찾으면:
           - after_keyword + 같은 줄: 키워드 뒤 데이터 추출
           - 그 외: 대상 라인 전체 반환
    """
    logging.debug(f"!!extract_data_from_text 시작: keyword: {keyword} extract_type: {extract_type} line_offset: {line_offset} separators: {separators}")

    lines = text.splitlines()
    # 빈 라인 제거
    lines = [line for line in lines if line.strip()]
    
    for i, line in enumerate(lines):
        found, matched_keyword = find_keyword_in_line(line, keyword)
        if found:
            target_line_index = i + line_offset
            
            # 라인 인덱스가 범위를 벗어나면 건너뜀
            if target_line_index < 0 or target_line_index >= len(lines):
                continue
                
            # 대상 라인 추출
            target_line = lines[target_line_index].strip()
            
            if extract_type == 'after_keyword' and line_offset == 0:
                result = extract_after_keyword(target_line, matched_keyword, separators)
                if result:  # 결과가 있으면 반환
                    return result
                # 결과가 없으면 계속 다음 매칭을 찾음
                continue
            else:
                logging.debug(f"!!extract_data_from_text 라인 전체 추출: {target_line}")
                return target_line
    
    return ""