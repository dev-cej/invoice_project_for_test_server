import json
import sys
import re
import logging
import os
from fuzzywuzzy import fuzz
backend_path = os.getenv('BACKEND_PATH')
constants_path = os.getenv('BACKEND_CONSTANTS_PATH')
config_path = os.getenv('CONFIG_PATH')
upload_path = os.getenv('UPLOAD_PATH')
sys.path.append(os.path.abspath(backend_path))
from config.logging_config import setup_logging
from DTO.response.py.TextExtractionResponse import TextExtractionResponseDTO
from DTO.detail.py.CaseNumberDTO import CaseNumberDTO
from DTO.detail.py.PayerCompanyDTO import PayerCompanyDTO
from DTO.detail.py.DateInfoDTO import DateInfoDTO
from DTO.detail.py.InvoiceNumberDTO import InvoiceNumberDTO
from utils.extract.filter_text import get_alternative_options
from services.extract.case_num.case_num import extract_case_number_from_text
from services.extract.match_company.match_company import find_similar_phrases_in_text, select_matched_candidate
from services.extract.invoice_num.invoice_num import extract_invoice_number_from_text
from services.extract.date.date import extract_dates_from_text, filter_primary_date
from DTO.detail.py.AmountBilledDTO import AmountBilledDTO, AmountDetail
from services.extract.amount.amount import extract_amounts_from_text

# 로깅 설정 초기화
setup_logging()


try:
    with open(constants_path + '/FileHandleStatus.json', 'r') as file:
        file_handle_status = json.load(file)
except Exception as e:
    logging.error("FileHandleStatus.json 파일을 읽는 중 오류 발생", exc_info=True)

def load_json_file(file_path):
    """JSON 파일을 로드하는 함수"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as e:
        logging.error(f"extract_text : 오류 발생: {str(e)}", exc_info=True)
        return {'status': 'error', 'message': f'오류 발생: {str(e)}'}


def main():
    logging.debug("extract_text.py 실행")
    try:
        # JSON 데이터 로드
        data = load_json_file(config_path + '/comany_info.json')
        company_code = None
        if 'status' in data and data['status'] == 'error':
            logging.error("extract_text : JSON 데이터 로드 실패")
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
        else:
            logging.warning("extract_text : 회사 정보를 찾을 수 없습니다.")    

        # 안건번호 및 송장번호 추출
        case_number,alternative_options = extract_case_number_from_text(text_content, company_code)

        case_number = [CaseNumberDTO.from_dict({
            'selected_candidate': number,
            'alternative_options': alternative_options
        }) for number in case_number]
        


        invoice_number, alternative_options = extract_invoice_number_from_text(text_content, company_code)
        invoice_number = [InvoiceNumberDTO(selected_candidate=number, alternative_options=alternative_options) for number in invoice_number]

        # 텍스트에서 날짜 추출
        dates = extract_dates_from_text(text_content)
        primary_date = filter_primary_date(dates, text_content)

        # primary_date를 제외한 alternative_options 생성
        alternative_dates = get_alternative_options(dates, [primary_date])
        date_info = [DateInfoDTO.from_dict({'selected_candidate': primary_date, 'alternative_options': alternative_dates})]

        # 청구 금액 추출
        amount_details, alternative_options = extract_amounts_from_text(text_content)
        
        # AmountBilledDTO에 맞게 데이터 구성
        amount_billed = AmountBilledDTO(
            selected_candidate=amount_details,
            alternative_options=alternative_options
        )

        # DTO 생성
        response_dto = TextExtractionResponseDTO(
            status= file_handle_status['STATUS_SUCCESS'],
            case_number=case_number[0] if case_number else None,
            payer_company=payer_company,
            invoice_number=invoice_number[0] if invoice_number else None,
            invoice_date=date_info[0] if date_info else None,
            amount_billed=amount_billed if amount_billed else None
        )
        # 결과 출력
        print(response_dto)
    except Exception as e:
        logging.critical("extract_text : 치명적인 오류 발생", exc_info=True)
        error_output = {
            'status': file_handle_status['STATUS_FAILURE'],
            'message': f'예외 발생: {str(e)}'
        }
        print(json.dumps(error_output, ensure_ascii=False))

if __name__ == "__main__":
    logging.debug("extract_text.py 실행")
    main()