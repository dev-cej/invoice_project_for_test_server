<?php
require_once Env::get('BACKEND_SERVICES_PATH') . '/PDFProcessing/PDFFileHandler.php';
require_once Env::get('BACKEND_SERVICES_PATH') . '/PDFProcessing/PDFConverter.php';
// error_reporting(E_ALL);
// ini_set('display_errors', 1);


function jsonResponse($success, $data) {
    return json_encode(array_merge(['success' => $success], $data), JSON_UNESCAPED_UNICODE);
}

function handlePDFToText() {

    try {
        $fileHandler = new PDFFileHandler();
        $file = $fileHandler->validateUploadedFile();
        $pdfPath = $fileHandler->savePDFFile($file);
        $hexPath = $fileHandler->handlePDFToHex($pdfPath);
        $pdfConverter = new PDFConverter($hexPath);
        $pdfConverter->handleConvertHexToText();
        // $pdfConverter->convertToAnalyzableFormat($hexPath);
        return jsonResponse(true, [
            'pdfPath' => $pdfPath,
            // 'analyzableFormatText' => $analyzableFormatText
        ]);
    } catch (Exception $e) {
        logGeneralError("error: " . $e->getMessage());
        return jsonResponse(false, ['error' => $e->getMessage()]);

    }

    // PDF 파일 저장
}

// API 엔드포인트 처리
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    header('Content-Type: application/json');
    echo handlePDFToText(); 
    exit;

}



