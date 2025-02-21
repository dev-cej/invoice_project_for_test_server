<?php
require_once Env::get('BACKEND_UTILS_PATH') . '/file/DirectoryHelper.php';
require_once Env::get('BACKEND_CONSTANTS_PATH') . '/path/PDFParserPathManager.php';
class PDFFileHandler {

    public function __construct() {
        $this->createDirectories();
        
    }

    private function createDirectories() {
        DirectoryHelper::createDirectoryIfNotExists(PDFParserPathManager::getPDFUploadPath());
        DirectoryHelper::createDirectoryIfNotExists(PDFParserPathManager::getDecompressedPath());
        DirectoryHelper::createDirectoryIfNotExists(PDFParserPathManager::getHexPath());

    }


    public function validateUploadedFile() {
        if (!isset($_FILES['pdf_file'])) {
            throw new Exception('PDF 파일이 없습니다.');
        }

        $file = $_FILES['pdf_file'];

        if ($file['error'] !== UPLOAD_ERR_OK) {
            throw new Exception('파일 업로드 실패: ' . $file['error']);
        }

        // MIME 타입 체크
        $finfo = finfo_open(FILEINFO_MIME_TYPE);
        $mimeType = finfo_file($finfo, $file['tmp_name']);
        finfo_close($finfo);

        if ($mimeType !== 'application/pdf') {
            throw new Exception('PDF 파일만 업로드 가능합니다.');
        }

        // PDF 헤더 체크
        $handle = fopen($file['tmp_name'], 'rb');
        $header = fread($handle, 4);
        fclose($handle);

        if ($header !== '%PDF') {
            throw new Exception('유효하지 않은 PDF 파일입니다.');
        }

        return $file;
    }


    public function savePDFFile($file) {
        $fileName = basename($file['name']);
        $filePath = PDFParserPathManager::getPDFUploadPath() . $fileName;
        if (!move_uploaded_file($file['tmp_name'], $filePath)) {
            throw new Exception('파일 저장 실패');
        }

        return $filePath;
    }

    public function handlePDFToHex($filePath) {
    // PDF 파일이 존재하는지 확인
    if (!file_exists($filePath)) {
            throw new Exception("파일을 찾을 수 없습니다: " . $filePath);
        }

            // PDF 파일을 바이너리 모드로 읽기
    $binaryData = file_get_contents($filePath);
    if ($binaryData === false) {
        throw new Exception("파일을 읽을 수 없습니다: " . $filePath);
    }

        // 바이너리 데이터를 16진수 문자열로 변환
        $hexData = strtoupper(bin2hex($binaryData));
        $outputPath = PDFParserPathManager::getHexPath() . basename($filePath, '.pdf') . '.hex';
        return $this->saveHexToFile($hexData, $outputPath);

    }
/**
 * 변환된 16진수 데이터를 파일로 저장하는 함수
 */
    public function saveHexToFile($hexData, $outputPath) {
        if (file_put_contents($outputPath, $hexData) === false) {
            throw new Exception("16진수 데이터를 파일로 저장하는 데 실패했습니다.");
        }

        return $outputPath;
}
}
