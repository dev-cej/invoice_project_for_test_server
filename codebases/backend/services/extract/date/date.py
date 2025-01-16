import re
from typing import List
import os
import sys
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging

setup_logging()

def extract_dates_from_text(text: str) -> List[str]:
    """텍스트에서 날짜를 추출하는 함수"""
    # 정규표현식 패턴 정의
    date_patterns = [
        r'\b\d{1,2}\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{4}\b',  # 예: "5 December 2024" 또는 "5 Dec 2024"
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{1,2},?\s*\d{4}\b',  # 예: "December 5, 2024" 또는 "Dec 5, 2024"
        r'\b\d{4}\s*/\s*\d{1,2}\s*/\s*\d{1,2}\b',  # 예: "2024/12/05"
        r'\b\d{1,2}\s*-\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s*-\s*\d{4}\b',  # 예: "05-Dec-2024"
        r'\d{4}年\s*\d{1,2}月\s*\d{1,2}日',         # 일본어
        r'\d{4}년\s*\d{1,2}월\s*\d{1,2}일',         # 한글
        r'\b\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{4}\b',  # 예: "12/05/2024"
        r'\b\d{1,2}\s*-\s*\d{1,2}\s*-\s*\d{4}\b',  # 예: "12-05-2024"
        r'\b\d{4}\s*-\s*\d{1,2}\s*-\s*\d{1,2}\b',  # 예: "2024-12-05"
        r'\b\d{1,2}\s*\.\s*\d{1,2}\s*\.\s*\d{4}\b',  # 예: "12.05.2024"
        r'\b\d{4}\s*\.\s*\d{1,2}\s*\.\s*\d{1,2}\b',  # 예: "2024.12.05"
    ]
    
    # 텍스트에서 날짜 패턴 매칭
    matches = []
    for pattern in date_patterns:
        matches.extend(re.findall(pattern, text))
    
    # 중복 제거
    unique_matches = list(set(matches))
    return unique_matches

def filter_primary_date(dates: List[str], context: str) -> str:
    """문맥에 따라 주요 날짜를 선택하는 함수"""
    # 문맥 기반 키워드
    keywords = ["Invoice", "請求", "청구서"]
    
    for date in dates:
        for keyword in keywords:
            if keyword in context:
                # 키워드와 날짜가 가까운 경우 해당 날짜를 반환
                if keyword in context.split(date)[0][-10:]:
                    return date
    # 기본적으로 첫 번째 날짜 반환
    return dates[0] if dates else None