import pdfplumber
import fitz  # PyMuPDF

def extract_text_with_positions(pdf_path):
    """PDF에서 텍스트와 위치 정보를 추출하는 함수."""
    text_items = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            for word in words:
                text = word['text']
                x0, top, x1, bottom = word['x0'], word['top'], word['x1'], word['bottom']
                text_items.append((text, (x0, top, x1, bottom)))
    return text_items

def highlight_text_on_specific_pages(pdf_path, output_path, text_items, pages_to_process):
    """여러 텍스트 항목에 대해 특정 페이지에 형광펜을 추가하는 함수."""
    doc = fitz.open(pdf_path)
    for page_number in pages_to_process:
        page = doc[page_number]
        for text, (x0, top, x1, bottom) in text_items:
            rect = fitz.Rect(x0, top, x1, bottom)
            highlight = page.add_highlight_annot(rect)
            highlight.update()
    doc.save(output_path, garbage=4, deflate=True, clean=True)