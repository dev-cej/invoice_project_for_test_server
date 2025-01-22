import pdfplumber
import json
import sys
import os
import logging
sys.path.append(os.path.abspath('/var/www/html/invoiceProject/codebases'))
from backend.DTO.detail.py.FileUploadDetail import FileUploadDetail
from backend.config.logging_config import setup_logging

# 로깅 설정 초기화
setup_logging()

# JSON 파일에서 상수 읽기
try:
    with open('/var/www/html/invoiceProject/codebases/backend/constants/FileType.json', 'r') as file:
        file_type = json.load(file)
except Exception as e:
    logging.error("FileType.json 파일을 읽는 중 오류 발생", exc_info=True)

try:
    with open('/var/www/html/invoiceProject/codebases/backend/constants/FileHandleStatus.json', 'r') as file:
        file_handle_status = json.load(file)
except Exception as e:
    logging.error("FileHandleStatus.json 파일을 읽는 중 오류 발생", exc_info=True)

def process_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text_found = False
            output_folder = "/var/www/html/invoiceProject/uploads/texts"
            os.makedirs(output_folder, exist_ok=True)
            
            # PDF 파일명에서 확장자 제거
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            text_file_path = os.path.join(output_folder, f"{base_filename}.txt")
            
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                for page_number, page in enumerate(pdf.pages):
                    text = page.extract_text(layout=True)
                    if text:
                        text_found = True
                        text_file.write(f"Page {page_number + 1}:\n{text}\n\n")
            
            if text_found:
                logging.debug(f"텍스트가 포함된 PDF 처리 성공: {file_path}")
                return FileUploadDetail(status=file_handle_status['STATUS_SUCCESS'], file_type=file_type['FILE_TYPE_TEXT']).to_dict()
            else:
                logging.warning(f"이미지로만 구성된 PDF: {file_path}")
                return FileUploadDetail(status=file_handle_status['STATUS_SUCCESS'], file_type=file_type['FILE_TYPE_IMAGE']).to_dict()

    except FileNotFoundError:
        logging.error(f"파일을 찾을 수 없습니다: {file_path}", exc_info=True)
        return FileUploadDetail(status=file_handle_status['STATUS_ERROR'], file_type=file_type['FILE_TYPE_UNKNOWN']).to_dict()

    except Exception as e:
        logging.error(f"PDF 처리 중 오류 발생: {file_path}", exc_info=True)
        return FileUploadDetail(status=file_handle_status['STATUS_ERROR'], file_type=file_type['FILE_TYPE_UNKNOWN']).to_dict()

if __name__ == '__main__':
    logging.debug("upload_file_handler.py 실행")
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = process_pdf(file_path)
        print(json.dumps(result))
    else:
        logging.error("파일 경로가 제공되지 않았습니다.")
        result = FileUploadDetail(status=file_handle_status['STATUS_ERROR'], file_type=file_type['FILE_TYPE_UNKNOWN']).to_dict()
        print(json.dumps(result))