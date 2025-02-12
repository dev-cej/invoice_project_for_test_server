<?php

class QDFParser {
    private $uploadDir;
    private $qdfOutputDir;
    private $textData;
    private $fontObjectIds;
    private $pageFontMappings;
    // 정규식 상수 정의
    private const FONT_BLOCK_REGEX = '/\/Font\s*<<\s*(.*?)\s*>>/s';
    private const FONT_REF_REGEX = '/\/(F\d+)\s+(\d+)\s+0\s+R/';
    private const OBJECT_BLOCK_REGEX_TEMPLATE = '/%s\s+0\s+obj(.*?)endobj/s';
    private const PAGE_OBJECT_REGEX = '/%% Page (\d+)\s*(\d+ \d+ obj\s*<<.*?>>\s*endobj)/s';

    private $fontMappings = [];

    public function __construct() {
        // 환경 변수에서 업로드 및 HEX 저장 경로 가져오기
        $this->uploadDir = Env::get('UPLOAD_PATH') . '/pdf/';
        $this->qdfOutputDir = Env::get('UPLOAD_PATH') . '/qdf/';

        // 디렉토리 생성
        $this->createDirectories();
    }

    private function createDirectories() {
        foreach ([$this->uploadDir, $this->qdfOutputDir] as $dir) {
            if (!file_exists($dir)) {
                mkdir($dir, 0777, true);
            }
        }
    }

    public function convertPDFToQDF() {
        try {
            // 파일 검증
            $file = $this->validateUploadedFile();

            // PDF 파일 저장
            $pdfPath = $this->savePDFFile($file);

            // PDF를 QDF로 변환
            $qdfPath = $this->convertToQDF($pdfPath);

            $this->textData = $this->extractTextFromQDF($qdfPath);

            // 폰트 매핑 추출
            $fontMappings = $this->extractFontMappings();


            return $this->jsonResponse(true, [
                'qdf_file' => basename($qdfPath),
                'text_data' => $textData
            ]);

        } catch (Exception $e) {
            return $this->jsonResponse(false, ['error' => $e->getMessage()]);
        }
    }


    private function extractTextFromQDF($qdfPath) {
        // QDF 파일 내용 읽기
        return file_get_contents($qdfPath);

        // 폰트 매핑 추출
    }

    private function validateUploadedFile() {
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

    private function savePDFFile($file) {
        $fileName = basename($file['name']);
        $filePath = $this->uploadDir . $fileName;
        if (!move_uploaded_file($file['tmp_name'], $filePath)) {
            throw new Exception('파일 저장 실패');
        }

        return $filePath;
    }

    private function convertToQDF($pdfPath) {
        // QPDF 설치 확인
        exec('which qpdf', $qpdfPath, $returnCode);
        if ($returnCode !== 0) {
            throw new Exception('QPDF가 설치되어 있지 않습니다.');
        }
        $qpdfPath = trim($qpdfPath[0]);

        // QDF 파일 경로 설정 (.qdf 확장자 사용)
        $qdfPath = $this->qdfOutputDir . uniqid('qdf_') . '.qdf';
        
        // PDF를 QDF로 변환
        $command = $qpdfPath . ' --qdf --no-original-object-ids ' . 
                  escapeshellarg($pdfPath) . ' ' . 
                  escapeshellarg($qdfPath) . ' 2>&1';
        
        exec($command, $output, $returnCode);
        
        if ($returnCode !== 0) {
            throw new Exception('QDF 변환 실패: ' . implode("\n", $output));
        }

        return $qdfPath;
    }



    private function extractPageContent($pdfPath, $objectId, &$textData) {
        // 4. 특정 객체의 내용 추출
        $command = sprintf('qpdf --show-object=%s "%s" 2>&1', $objectId, $pdfPath);
        exec($command, $output, $returnCode);

        if ($returnCode !== 0) {
            throw new Exception('컨텐츠 스트림 추출 실패');
        }

        $inStream = false;
        $currentStream = '';

        foreach ($output as $line) {
            // 5. 스트림 데이터 수집
            if (strpos($line, 'stream') !== false) {
                $inStream = true;
                continue;
            }

            if (strpos($line, 'endstream') !== false) {
                $inStream = false;
                $this->parseContentStream($currentStream, $textData);
                $currentStream = '';
                continue;
            }

            if ($inStream) {
                $currentStream .= $line;
            }
        }
    }

    private function parseContentStream($stream, &$textData) {
        // 6. Tj 및 TJ 연산자 찾기
        preg_match_all('/\((.*?)\)\s*Tj|\[(.*?)\]\s*TJ/', $stream, $matches);

        foreach ($matches[0] as $match) {
            // 7. TJ 연산자 처리
            if (strpos($match, 'TJ') !== false) {
                preg_match_all('/\((.*?)\)/', $match, $tjMatches);
                foreach ($tjMatches[1] as $text) {
                    $this->processText($text, $textData);
                }
            } 
            // 8. Tj 연산자 처리
            else {
                preg_match('/\((.*?)\)/', $match, $tjMatch);
                if (!empty($tjMatch[1])) {
                    $this->processText($tjMatch[1], $textData);
                }
            }
        }
    }

    private function processText($text, &$textData) {
        // 9. UTF-16BE 인코딩 확인 및 변환
        if (substr($text, 0, 2) === "\xFE\xFF") {
            $text = mb_convert_encoding(substr($text, 2), 'UTF-8', 'UTF-16BE');
        }
        
        // 10. 유효한 텍스트만 저장
        if (!empty(trim($text))) {
            $textData[] = trim($text);
        }
    }

    public function getHexFile($fileName) {
        $filePath = $this->hexOutputDir . $fileName;

        if (!file_exists($filePath)) {
            throw new Exception('HEX 파일을 찾을 수 없습니다.');
        }

        return file_get_contents($filePath);
    }

    private function jsonResponse($success, $data) {
        return json_encode(array_merge(['success' => $success], $data), JSON_UNESCAPED_UNICODE);
    }

    private function extractPageObject() {
        preg_match_all(self::PAGE_OBJECT_REGEX, $this->textData, $pageObjects);
        logGeneralError("pageObjects: " . json_encode($pageObjects));
        return $pageObjects;
    }

    private function extractFontMappings() {
        // 페이지별 폰트 매핑 저장
        $pageObjects = $this->extractPageObject();
        // 모든 폰트 매핑 블록 추출
        preg_match_all(self::FONT_BLOCK_REGEX, $this->textData, $fontBlocks);

        if (empty($fontBlocks[1])) {
            throw new Exception('폰트 매핑을 찾을 수 없습니다.');
        }

        // 각 폰트 매핑 블록에 대해 폰트 객체 참조 추출
        foreach ($fontBlocks[1] as $fontBlock) {
            preg_match_all(self::FONT_REF_REGEX, $fontBlock, $fontRefs);
            logGeneralError("fontRefs: " . json_encode($fontRefs));

            // foreach ($fontRefs[1] as $index => $fontName) {
            //     $objectId = $fontRefs[2][$index];
            //     logGeneralError("objectId: " . $objectId);
            //     $index = $fontRefs[3][$index];
            //     logGeneralError("index: " . $index);
            //     // 페이지 번호를 추출하는 로직 필요 (예: $currentPage)
            //     $currentPage = $this->getCurrentPage($fontBlock); // 페이지 번호 추출 로직 구현 필요

            //     if (!isset($this->pageFontMappings[$currentPage])) {
            //         $this->pageFontMappings[$currentPage] = [];
            //     }

            //     $this->pageFontMappings[$currentPage][$fontName] = [
            //         'object_id' => $objectId,
            //         'index' => $index,
            //     ];
            // }
            }

        
            return $this->pageFontMappings;
    }
}

// API 엔드포인트 처리
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    header('Content-Type: application/json');

    $converter = new QDFParser();
    echo $converter->convertPDFToQDF();
    exit;
}



