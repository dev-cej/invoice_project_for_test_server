import json
import sys
import re
import logging
import os
from fuzzywuzzy import fuzz
from typing import List, Dict
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging
from backend.DTO.response.py.TextExtractionResponse import TextExtractionResponseDTO
from backend.DTO.detail.py.CaseNumberDTO import CaseNumberDTO
from backend.DTO.detail.py.PayerCompanyDTO import PayerCompanyDTO
from backend.DTO.detail.py.DateInfoDTO import DateInfoDTO
from backend.DTO.detail.py.InvoiceNumberDTO import InvoiceNumberDTO
from backend.utils.extract.filter_text import get_alternative_options
from backend.services.extract.case_num.case_num import extract_case_numbers_from_text, filter_case_numbers_by_context
from backend.services.extract.match_company.match_company import find_similar_phrases_in_text, select_matched_candidate
from backend.services.extract.invoice_num.invoice_num import extract_invoice_number_from_text
from backend.services.extract.date.date import extract_dates_from_text, filter_primary_date
from backend.DTO.detail.py.AmountBilledDTO import AmountBilledDTO, AmountDetail
from backend.services.extract.amount.amount import extract_amounts_from_text

# 로깅 설정 초기화
setup_logging()


try:
    with open('/var/www/html/invoiceProject/codebases/backend/constants/FileHandleStatus.json', 'r') as file:
        file_handle_status = json.load(file)
except Exception as e:
    logging.error("FileHandleStatus.json 파일을 읽는 중 오류 발생", exc_info=True)

def load_json_file(file_path):
    """JSON 파일을 로드하는 함수"""
    logging.debug(f"load_json_file 시작: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logging.debug("JSON 파일 로드 성공")
            return data
    except Exception as e:
        logging.error(f"오류 발생: {str(e)}", exc_info=True)
        return {'status': 'error', 'message': f'오류 발생: {str(e)}'}


def main():
    logging.debug("main 함수 시작")
    try:
        # JSON 데이터 로드
        data = load_json_file('/var/www/html/invoiceProject/codebases/backend/config/comany_info.json')
        company_code = None
        if 'status' in data and data['status'] == 'error':
            logging.error("JSON 데이터 로드 실패")
            print(json.dumps(data, ensure_ascii=False))
            return
        
        # 텍스트 파일 경로를 인자로 받음
        text_file_path = sys.argv[1]
        with open(text_file_path, 'r', encoding='utf-8') as text_file:
            text_content = text_file.read()


            
        # PayerCompanyDTO에 맞게 데이터 구성
        similar_phrases = find_similar_phrases_in_text(text_content, data['companies'])
        matched_candidate, alternative_options = select_matched_candidate(similar_phrases)
        payer_company = PayerCompanyDTO.from_dict({
            'matched_candidate': {
                'matched_phrase': matched_candidate['phrase'] if matched_candidate else None,
                'matched_master_data': matched_candidate['company'] if matched_candidate else None,
                'similarity': matched_candidate['similarity'] if matched_candidate else None,
                'match_type': matched_candidate['preferred'] if matched_candidate else None
            },
            'alternative_options': [
                {
                    'matched_phrase': alternative_option['phrase'] if alternative_option else None,
                    'matched_master_data': alternative_option['company'] if alternative_option else None,
                    'similarity': alternative_option['similarity'] if alternative_option else None,
                    'match_type': alternative_option['preferred'] if alternative_option else None
                } for alternative_option in alternative_options
            ]
        })

        if matched_candidate:
            company_code = matched_candidate['company']['code']
            logging.info(f"추출된 회사코드: {company_code}")
        else:
            logging.warning("회사 정보를 찾을 수 없습니다.")    


        # 안건번호 및 송장번호 추출
        raw_case_numbers = extract_case_numbers_from_text(text_content)
        filtered_case_numbers = filter_case_numbers_by_context(text_content, raw_case_numbers)
        
        # 필터링된 후보를 제외한 나머지 후보를 alternative_options에 저장
        alternative_options = get_alternative_options(raw_case_numbers, filtered_case_numbers)
        
        case_number = [CaseNumberDTO.from_dict({
            'selected_candidate': number,
            'alternative_options': alternative_options
        }) for number in filtered_case_numbers]

        logging.info(f"추출된 안건번호!: {case_number}")


        invoice_number, alternative_options = extract_invoice_number_from_text(text_content, company_code)
        invoice_number = [InvoiceNumberDTO(selected_candidate=number, alternative_options=alternative_options) for number in invoice_number]
        logging.info(f"추출된 송장번호: {invoice_number}")

        # 텍스트에서 날짜 추출
        dates = extract_dates_from_text(text_content)
        primary_date = filter_primary_date(dates, text_content)

        # primary_date를 제외한 alternative_options 생성
        alternative_dates = get_alternative_options(dates, [primary_date])
        date_info = [DateInfoDTO.from_dict({'selected_candidate': primary_date, 'alternative_options': alternative_dates})]
        logging.info(f"추출된 날짜 정보: {date_info}")

        # 청구 금액 추출
        amount_details, alternative_options = extract_amounts_from_text(text_content)
        logging.info(f"추출된 청구 금액: {amount_details}, {alternative_options}")
        
        # AmountBilledDTO에 맞게 데이터 구성
        amount_billed = AmountBilledDTO(
            selected_candidate=amount_details,
            alternative_options=alternative_options
        )
        logging.info(f"추출된 청구 금액: {amount_billed.to_dict()}")

        # DTO 생성
        response_dto = TextExtractionResponseDTO(
            status= file_handle_status['STATUS_SUCCESS'],
            case_number=case_number[0] if case_number else None,
            payer_company=payer_company,
            invoice_number=invoice_number[0] if invoice_number else None,
            invoice_date=date_info[0] if date_info else None,
            amount_billed=amount_billed if amount_billed else None
        )
        logging.info(f"추출된 결과: {response_dto}")
        # 결과 출력
        logging.info("결과 생성 성공")
        print(response_dto)
    except Exception as e:
        logging.critical("치명적인 오류 발생", exc_info=True)
        error_output = {
            'status': file_handle_status['STATUS_FAILURE'],
            'message': f'예외 발생: {str(e)}'
        }
        print(json.dumps(error_output, ensure_ascii=False))

if __name__ == "__main__":
    logging.debug("extract_text.py 실행")
    main()