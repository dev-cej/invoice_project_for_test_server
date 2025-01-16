import pdfplumber
import fitz  # PyMuPDF
import sys
import json
import logging
import os
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging
from backend.DTO.response.py.TextExtractionResponse import TextExtractionResponseDTO

class PDFHighlighter:
    def __init__(self, output_directory):
        self.output_directory = output_directory
        self.setup_output_directory()
        setup_logging()

    def setup_output_directory(self):
        try:
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory, mode=0o755)  # 적절한 권한 설정
            os.chmod(self.output_directory, 0o755)  # 디렉토리 권한 확인
        except Exception as e:
            logging.error(f"디렉토리 생성/권한 설정 실패: {str(e)}", exc_info=True)
            raise

    def parse_extracted_data(self, extractResults):
        """JSON 문자열을 파싱하여 TextExtractionResponseDTO 객체 리스트를 반환합니다."""
        logging.debug(f"PDF 파일 경로: {extractResults}")
        data_list = json.loads(extractResults)
        return [TextExtractionResponseDTO.from_dict(data) for data in data_list]

    def add_to_highlight_list(self, source, target_list):
        """source가 리스트인지 문자열인지 확인하여 target_list에 추가"""
        if isinstance(source, list):
            target_list.extend(source)
        else:
            target_list.append(source)

    def extract_highlight_texts(self, data_item):
        """TextExtractionResponseDTO 객체에서 하이라이트할 텍스트를 추출합니다."""
        highlight_texts = {
            "selected": [],
            "alternative": []
        }
        
        # 각 속성에 대해 add_to_highlight_list 함수를 사용하여 중복 제거
        if data_item.case_number.selected_candidate:
            self.add_to_highlight_list(data_item.case_number.selected_candidate, highlight_texts["selected"])
        
        if data_item.case_number.alternative_options:
            self.add_to_highlight_list(data_item.case_number.alternative_options, highlight_texts["alternative"])

        # payer_company의 matched_candidate와 alternative_options 처리
        if data_item.payer_company.matched_candidate:
            # matched_candidate의 matched_phrase를 selected에 추가
            matched_phrase = data_item.payer_company.matched_candidate.matched_phrase
            highlight_texts["selected"].append(matched_phrase)

        if data_item.payer_company.alternative_options:
            # 각 alternative_option의 matched_phrase를 alternative에 추가
            for option in data_item.payer_company.alternative_options:
                highlight_texts["alternative"].append(option.matched_phrase)

        if data_item.invoice_date.selected_candidate:
            self.add_to_highlight_list(data_item.invoice_date.selected_candidate, highlight_texts["selected"])
        
        if data_item.invoice_date.alternative_options:
            self.add_to_highlight_list(data_item.invoice_date.alternative_options, highlight_texts["alternative"])

        if data_item.invoice_number.selected_candidate:
            self.add_to_highlight_list(data_item.invoice_number.selected_candidate, highlight_texts["selected"])
        
        if data_item.invoice_number.alternative_options:
            self.add_to_highlight_list(data_item.invoice_number.alternative_options, highlight_texts["alternative"])

        logging.debug(f"highlight_texts: {highlight_texts}")

        return highlight_texts

    def highlight_text_in_pdf_by_search(self, pdf_path, output_path, search_texts, color):
        """PDF에서 특정 텍스트를 검색하여 하이라이트하는 함수."""
        logging.debug(f"PDF 파일에 하이라이트 추가 시작: {pdf_path}")
        try:
            doc = fitz.open(pdf_path)
            for page_number in range(len(doc)):
                page = doc[page_number]
                logging.debug(f"페이지 번호: {page_number} 처리 중")
                for search_text in search_texts:
                    logging.debug(f"검색할 텍스트: '{search_text}'")
                    text_instances = page.search_for(search_text)
                    if not text_instances:
                        logging.warning(f"텍스트를 찾을 수 없음: '{search_text}' - 페이지: {page_number}")
                    for inst in text_instances:
                        logging.debug(f"텍스트 인스턴스 발견: {inst}")
                        highlight = page.add_highlight_annot(inst)
                        highlight.set_colors(stroke=color, fill=color)  # 하이라이트 색상 및 투명도 설정
                        highlight.set_opacity(0.5)  # 투명도 설정
                        highlight.update()
            doc.save(output_path, garbage=4, deflate=True, clean=True)
            logging.info(f"하이라이트된 PDF 저장 완료: {output_path}")
        except Exception as e:
            logging.error(f"하이라이트 추가 중 오류 발생: {str(e)}", exc_info=True)

    def highlight_texts_in_pdf(self, pdf_path, highlight_texts):
        """PDF에서 텍스트를 하이라이트합니다."""
        logging.debug(f"highlight_texts_in_pdf 시작: {pdf_path}")
        logging.debug(f"highlight_texts: {highlight_texts}")
        # 파일명에서 확장자를 제거하고, 하이라이트된 파일명 생성
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        intermediate_path = os.path.join(self.output_directory, f'{base_name}_intermediate.pdf')
        output_path = os.path.join(self.output_directory, f'{base_name}_highlighted.pdf')

        # 형광 핑크로 selected_candidate 하이라이트
        self.highlight_text_in_pdf_by_search(pdf_path, intermediate_path, highlight_texts["selected"], color=(1, 0, 1))  # RGB: 형광 핑크

        # 중간 저장된 파일을 다시 열어 연한 노랑으로 alternative_options 하이라이트
        self.highlight_text_in_pdf_by_search(intermediate_path, output_path, highlight_texts["alternative"], color=(1, 1, 0.5))  # RGB: 연한 노랑

def main():
    try:
        logging.debug("하이라이트 작업 시작")
        extractResults = sys.argv[1]  # JSON 문자열
        highlighter = PDFHighlighter('/var/www/html/invoiceProject/uploads/highlight/')
        extracted_data = highlighter.parse_extracted_data(extractResults)

        for data_item in extracted_data:
            # PDF 파일 경로 설정
            pdf_path = os.path.join('/var/www/html/invoiceProject/uploads/pdfs/', data_item.file_name)
            logging.debug(f"처리할 PDF 파일: {pdf_path}")
            
            # 파일 존재 여부 확인
            if not os.path.exists(pdf_path):
                logging.error(f"파일이 존재하지 않습니다: {pdf_path}")
                continue

            highlight_texts = highlighter.extract_highlight_texts(data_item)
            highlighter.highlight_texts_in_pdf(pdf_path, highlight_texts)

    except Exception as e:
        logging.error(f"하이라이트 작업 중 예외 발생: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()