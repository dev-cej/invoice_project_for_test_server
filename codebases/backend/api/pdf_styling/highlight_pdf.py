import pdfplumber
import fitz  # PyMuPDF
import sys
import json
import logging
import os
backend_path = os.getenv('BACKEND_PATH')
upload_path = os.getenv('UPLOAD_PATH')
backend_api_path = os.getenv('BACKEND_API_PATH')
sys.path.append(os.path.abspath(backend_path))
from config.logging_config import setup_logging
from DTO.response.py.TextExtractionResponse import TextExtractionResponseDTO

setup_logging()


class PDFHighlighter:
    def __init__(self, output_directory):
        self.output_directory = output_directory
        logging.debug(f'output_directory: {self.output_directory}')
        self.setup_output_directory()

    def setup_output_directory(self):
        try:
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory, exist_ok=True)
            # 현재 권한 확인
        except Exception as e:
            logging.error(f'Error in setup_output_directory: {e}')
            raise

    def parse_extracted_data(self, extractResults):
        logging.debug('parse_extracted_data 실행')
        """JSON 문자열을 파싱하여 TextExtractionResponseDTO 객체 리스트를 반환합니다."""
        data_list = json.loads(extractResults)
        return [TextExtractionResponseDTO.from_dict(data) for data in data_list]

    def add_to_highlight_list(self, source, target_list):
        """source가 리스트인지 문자열인지 확인하여 target_list에 추가"""
        if source:  # 데이터가 있는지 확인
            if isinstance(source, list):
                target_list.extend(source)
            else:
                target_list.append(source)

    def extract_highlight_texts(self, data_item):
        """TextExtractionResponseDTO 객체에서 하이라이트할 텍스트를 추출합니다."""
        logging.debug('extract_highlight_texts 실행' + str(data_item))
        highlight_texts = {
            "case_number": {"selected": [], "alternative": []},
            "invoice_date": {"selected": [], "alternative": []},
            "invoice_number": {"selected": [], "alternative": []},
            "payer_company": {"selected": [], "alternative": []},
            "amount_billed": {"selected": [], "alternative": []}
        }
        
        # 각 속성에 대해 add_to_highlight_list 함수를 사용하여 중복 제거
        self.add_to_highlight_list(data_item.case_number.selected_candidate, highlight_texts["case_number"]["selected"])
        self.add_to_highlight_list(data_item.case_number.alternative_options[:3], highlight_texts["case_number"]["alternative"])
        self.add_to_highlight_list(data_item.invoice_date.selected_candidate, highlight_texts["invoice_date"]["selected"])
        self.add_to_highlight_list(data_item.invoice_date.alternative_options[:3], highlight_texts["invoice_date"]["alternative"])
        self.add_to_highlight_list(data_item.invoice_number.selected_candidate, highlight_texts["invoice_number"]["selected"])
        self.add_to_highlight_list(data_item.invoice_number.alternative_options[:3], highlight_texts["invoice_number"]["alternative"])

        # payer_company의 matched_candidate와 alternative_options 처리
        if data_item.payer_company.matched_candidate:
            highlight_texts["payer_company"]["selected"].append(data_item.payer_company.matched_candidate.matched_phrase)
        for option in data_item.payer_company.alternative_options[:3]:
            highlight_texts["payer_company"]["alternative"].append(option.matched_phrase)
        # AmountBilledDTO의 데이터를 처리
        for candidate in data_item.amount_billed.selected_candidate:
            highlight_texts["amount_billed"]["selected"].append(candidate.amount)
        for option in data_item.amount_billed.alternative_options[:3]:
            highlight_texts["amount_billed"]["alternative"].append(option.amount)
        return highlight_texts

    def highlight_texts_in_pdf(self, pdf_path, highlight_texts):
        """PDF에서 텍스트를 하이라이트하거나 밑줄을 긋습니다."""
        output_path = os.path.join(self.output_directory, f'{os.path.splitext(os.path.basename(pdf_path))[0]}_highlighted.pdf')
        logging.debug(f'pdf_path: {pdf_path}')
        logging.debug(f'output_path: {output_path}')

        # 색상 팔레트
        color_map = {
            "case_number": {"selected": (1.0, 0.6, 0.6), "alternative": (1.0, 0.0, 0.0)},  # 진한 빨강
            "invoice_date": {"selected": (0.6, 1.0, 0.6), "alternative": (0.113, 0.85, 0.086)},  # 진한 초록
            "invoice_number": {"selected": (0.4, 0.6, 1.0), "alternative": (0.01, 0.0, 1.0)},  # 진한 파랑
            "payer_company": {"selected": (1.0, 1.0, 0.0), "alternative": (1.0, 0.8, 0.07)},  # 진한 노랑
            "amount_billed": {"selected": (1.0, 0.7, 0.5), "alternative": (1.0, 0.36, 0.0)}  # 진한 주황
        }

        try:
            doc = fitz.open(pdf_path)
            for page_number, page in enumerate(doc):
                logging.debug(f'Processing page {page_number + 1}')
                for category, texts in highlight_texts.items():
                    logging.debug(f'Category: {category}')
                    # None 체크 추가
                    selected_texts = texts["selected"] or []
                    alternative_texts = texts["alternative"] or []
                    
                    for search_text in selected_texts:
                        if not search_text:  # None이나 빈 문자열 건너뛰기
                            continue
                        logging.debug(f'Searching for selected text: {search_text}')
                        text_instances = page.search_for(str(search_text))  # 문자열로 변환
                        for inst in text_instances:
                            logging.debug(f'Highlighting text at: {inst}')
                            highlight = page.add_highlight_annot(inst)
                            highlight.set_colors(stroke=color_map[category]["selected"], fill=color_map[category]["selected"])
                            highlight.update()
                            
                    for search_text in alternative_texts:
                        if not search_text:  # None이나 빈 문자열 건너뛰기
                            continue
                        logging.debug(f'Searching for alternative text: {search_text}')
                        text_instances = page.search_for(str(search_text))  # 문자열로 변환
                        for inst in text_instances:
                            logging.debug(f'Adding squiggly underline at: {inst}')
                            squiggly = page.add_squiggly_annot(inst)
                            squiggly.set_colors(stroke=color_map[category]["alternative"])
                            squiggly.update()
            doc.save(output_path, garbage=4, deflate=True, clean=True)
            doc.close()
        except Exception as e:
            logging.error(f'Error processing PDF: {e}')

def main():
    try:
        logging.debug('highlight_pdf.py 실행')
        extractResults = sys.argv[1]  # JSON 문자열
        highlighter = PDFHighlighter(upload_path + '/highlight/')
        extracted_data = highlighter.parse_extracted_data(extractResults)
        for data_item in extracted_data:
            logging.debug(f'data_item: {data_item}')
            # PDF 파일 경로 설정
            pdf_path = os.path.join(upload_path + '/pdfs/', data_item.file_name)
            
            # 파일 존재 여부 확인
            if not os.path.exists(pdf_path):
                continue

            highlight_texts = highlighter.extract_highlight_texts(data_item)
            highlighter.highlight_texts_in_pdf(pdf_path, highlight_texts)
    except Exception as e:
        logging.error(f'Error in main: {e}')
        pass

if __name__ == "__main__":
    main()