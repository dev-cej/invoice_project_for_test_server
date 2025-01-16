import re
import logging
import os
import sys
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging


# 로깅 설정 초기화
setup_logging()

def extract_case_numbers_from_text(text):
    """텍스트에서 안건번호를 추출하는 함수"""
    # T는 그대로, M과 D 뒤에는 영문자가 올 수 있게 수정
    pattern = r'\b(?:T|M[A-Z]?|D[A-Z]?)[A-Z0-9-]*\d+[A-Z0-9-]*-[A-Z0-9-]*\b|\b(?:T|M[A-Z]?|D[A-Z]?)[A-Z0-9-]*-[A-Z0-9-]*\d+[A-Z0-9-]*\b'
    matches = re.findall(pattern, text)
    return list(set(matches))

def filter_case_numbers_by_context(text, candidates):
    # logging.debug(f"filter_case_numbers_by_context 시작: {candidates}")
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



