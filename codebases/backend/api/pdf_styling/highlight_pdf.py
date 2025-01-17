import pdfplumber
import fitz  # PyMuPDF
import sys
import json
import logging
import os
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.config.logging_config import setup_logging
from backend.DTO.response.py.TextExtractionResponse import TextExtractionResponseDTO

setup_logging()


class PDFHighlighter:
    def __init__(self, output_directory):
        self.output_directory = output_directory
        self.setup_output_directory()

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
        logging.debug(f"extractResults: {extractResults}")
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

        logging.debug(f"highlight_texts: {highlight_texts}")
        return highlight_texts

    def highlight_text_in_pdf_by_search(self, pdf_path, output_path, search_texts, color):
        """PDF에서 특정 텍스트를 검색하여 하이라이트하는 함수."""
        logging.debug(f"PDF 파일에 하이라이트 추가 시작: search_texts: {search_texts}")
        try:
            doc = fitz.open(pdf_path)
            for page_number, page in enumerate(doc):
                logging.debug(f"페이지 번호: {page_number} 처리 중")
                for search_text in search_texts:
                    logging.debug(f"검색할 텍스트: '{search_text}'")
                    text_instances = page.search_for(search_text)
                    if not text_instances:
                        logging.warning(f"텍스트를 찾을 수 없음: '{search_text}' - 페이지: {page_number}")
                    for inst in text_instances:
                        logging.debug(f"텍스트 인스턴스 발견: {inst}")
                        highlight = page.add_highlight_annot(inst)
                        highlight.set_colors(stroke=color, fill=color)
                        highlight.set_opacity(0.5)
                        highlight.update()
            doc.save(output_path, garbage=4, deflate=True, clean=True)
            doc.close()  # 파일 닫기
            logging.info(f"하이라이트된 PDF 저장 완료: {output_path}")
        except Exception as e:
            logging.error(f"하이라이트 추가 중 오류 발생: {str(e)}", exc_info=True)


    def highlight_texts_in_pdf(self, pdf_path, highlight_texts):
        """PDF에서 텍스트를 하이라이트합니다."""
        logging.debug(f"highlight_texts_in_pdf 시작: {pdf_path}")
        logging.debug(f"highlight_texts: {highlight_texts}")
        output_path = os.path.join(self.output_directory, f'{os.path.splitext(os.path.basename(pdf_path))[0]}_highlighted.pdf')

        # 조화로운 파스텔 색상 팔레트
        color_map = {
            "case_number": {"selected": (1.0, 0.6, 0.6), "alternative": (1.0, 0.8, 0.8)},  # 밝은 빨강
            "invoice_date": {"selected": (0.6, 1.0, 0.6), "alternative": (0.8, 1.0, 0.8)},  # 밝은 초록
            "invoice_number": {"selected": (0.4, 0.6, 1.0), "alternative": (0.6, 0.8, 1.0)},  # 밝은 파랑
        "payer_company": {"selected": (1.0, 1.0, 0.0), "alternative": (1.0, 1.0, 0.5)},  # 형광 노랑
            "amount_billed": {"selected": (1.0, 0.7, 0.5), "alternative": (1.0, 0.85, 0.7)}  # 밝은 주황
        }

        try:
            doc = fitz.open(pdf_path)
            for page_number, page in enumerate(doc):
                logging.debug(f"페이지 번호: {page_number} 처리 중")
                for category, texts in highlight_texts.items():
                    for search_text in texts["selected"]:
                        logging.debug(f"검색할 텍스트: '{search_text}'")
                        text_instances = page.search_for(search_text)
                        for inst in text_instances:
                            highlight = page.add_highlight_annot(inst)
                            highlight.set_colors(stroke=color_map[category]["selected"], fill=color_map[category]["selected"])
                            highlight.set_opacity(0.9)  # 진한 색상은 덜 투명하게
                            highlight.update()
                    for search_text in texts["alternative"]:
                        logging.debug(f"검색할 텍스트: '{search_text}'")
                        text_instances = page.search_for(search_text)
                        for inst in text_instances:
                            highlight = page.add_highlight_annot(inst)
                            highlight.set_colors(stroke=color_map[category]["alternative"], fill=color_map[category]["alternative"])
                            highlight.set_opacity(0.5)  # 연한 색상은 더 투명하게
                            highlight.update()
            doc.save(output_path, garbage=4, deflate=True, clean=True)
            doc.close()
            logging.info(f"하이라이트된 PDF 저장 완료: {output_path}")
        except Exception as e:
            logging.error(f"하이라이트 추가 중 오류 발생: {str(e)}", exc_info=True)

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