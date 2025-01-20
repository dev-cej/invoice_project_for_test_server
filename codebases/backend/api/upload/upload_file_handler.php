<?php
// CORS 헤더 설정
if (isset($_SERVER['HTTP_ORIGIN']) && ($_SERVER['HTTP_ORIGIN'] == 'https://www.ktainvoice.o-r.kr')) {
    header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
    header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
    header("Access-Control-Allow-Headers: Origin, Content-Type, Accept, Authorization");
}

// Content-Type을 JSON으로 설정
header('Content-Type: application/json');

// 로그 함수 포함
require_once('/var/www/html/invoiceProject/codebases/backend/config/config.php');

require_once('/var/www/html/invoiceProject/codebases/backend/DTO/response/php/FileUploadResponse.php');
require_once('/var/www/html/invoiceProject/codebases/backend/DTO/response/php/ApiResponse.php');
require_once('/var/www/html/invoiceProject/codebases/backend/DTO/detail/php/FileUploadDetail.php');
require_once('/var/www/html/invoiceProject/codebases/backend/DTO/detail/php/ExtractResult.php');

// JSON 파일에서 상수 읽기
$jsonString = file_get_contents('/var/www/html/invoiceProject/codebases/backend/constants/FileType.json');
$fileType = json_decode($jsonString, true);
$jsonString = file_get_contents('/var/www/html/invoiceProject/codebases/backend/constants/FileHandleStatus.json');
$fileHandleStatus = json_decode($jsonString, true);

// Python 스크립트의 절대 경로
$scriptPath = '/var/www/html/invoiceProject/codebases/backend/api/upload/upload_file_handler.py';
$extractScriptPath = '/var/www/html/invoiceProject/codebases/backend/api/extract/extract_text.py';
$highlightScriptPath = '/var/www/html/invoiceProject/codebases/backend/api/pdf_styling/highlight_pdf.py';
$textDirPath = "/var/www/html/invoiceProject/uploads/texts/";
$uploadDir = '/var/www/html/invoiceProject/uploads/pdfs/';
$uploadedFiles = [];
$responseData = [];

// 디렉토리가 존재하지 않으면 생성
if (!is_dir($uploadDir)) {
    if (!mkdir($uploadDir, 0770, true)) {
        error_log("Failed to create directory: $uploadDir");
    }
}

try {
    // 업로드된 파일의 개수 로그 기록
    $fileCount = count($_FILES['files']['tmp_name']);
    logGeneralError("!!업로드된 파일 개수: $fileCount");

    // 파일 업로드 처리
    logGeneralError("파일 업로드 처리 시작");
    foreach ($_FILES['files']['tmp_name'] as $key => $tmpName) {

        $fileName = basename($_FILES['files']['name'][$key]);
        $filePath = $uploadDir . $fileName;
        // 임시로 파일을 저장
        if (move_uploaded_file($tmpName, $filePath)) {
            // Python 스크립트 실행
            logGeneralError("Python 스크립트 실행");
            // 파일 경로를 따옴표로 감싸서 전달
            $escapedFilePath = escapeshellarg($filePath);
            $command = "$pythonPath $scriptPath $escapedFilePath";
            logGeneralError("!!Python 스크립트 호출: $command");
            $output = shell_exec($command . " 2>&1");

            if ($output === null) {
                logGeneralError("Python 스크립트 실행 실패: $command");
            } else {
                logGeneralError("Python 스크립트 출력: " . $output);
            }
            $result = json_decode($output, true);

            logGeneralError("파일 업로드 스크립트 결과 :", $result);

            if ($result === null) {
                logGeneralError("파이썬 스크립트 오류: " . json_last_error_msg());
                throw new Exception("파이썬 스크립트 오류: " . json_last_error_msg());
            }

            // 파일 유형에 따라 처리
            if ($result['fileType'] === $fileType['FILE_TYPE_TEXT']) {
                $baseFileName = pathinfo($fileName, PATHINFO_FILENAME);
                $extractFilePath = $textDirPath . $baseFileName . ".txt";
                $escapedExtractFilePath = escapeshellarg($extractFilePath);

                // 텍스트 파일인 경우 추출 작업 수행
                logGeneralError("!!텍스트 파일인 경우 추출 작업 수행");
                $extractCommand = "$pythonPath $extractScriptPath $escapedExtractFilePath";
                $extractOutput = shell_exec($extractCommand . " 2>&1");

                if ($extractOutput === null) {
                    logGeneralError("Python 스크립트 실행 실패: $extractCommand");
                } else {
                    logGeneralError("텍스트 결과: " . $extractOutput);
                }
                $extractResult = json_decode($extractOutput, true);
                
                if ($extractResult['status'] === 'success') {

                    $extractResultObject = ExtractResult::fromArray($extractResult);
                    logGeneralError("!!추출 결과 객체: " . $extractResultObject->toExtractResultArray());
                    $extractResultObject->setFileName($fileName);
                    $extractResultObject->setFileType($fileType['FILE_TYPE_TEXT']);
                    $extractResults[] = $extractResultObject;
                    
                } else {
                    $extractResults[] = new ExtractResult($fileName, $fileHandleStatus['STATUS_FAILURE'], $fileType['FILE_TYPE_TEXT'], null, null, null, null, null, null);
                }
            }
            else if  ($fileType['FILE_TYPE_IMAGE'] === $result['fileType'] ) {
                $extractResults[] = new ExtractResult($fileName, $fileHandleStatus['STATUS_SUCCESS'], $fileType['FILE_TYPE_IMAGE'], null, null, null, null, null, null);
                // 이미지 파일인 경우

            }
            else {
                $error = error_get_last();
                logGeneralError($filePath, $error ? $error['message'] : '파일 유형 오류');
                $extractResults[] = new ExtractResult($fileName, $fileHandleStatus['STATUS_FAILURE'], $fileType['FILE_TYPE_UNKNOWN'], null, null, null, null, null, null);
            }
        } 
        else {
            $error = error_get_last();
            logGeneralError($filePath, $error ? $error['message'] : '파일 업로드 실패');
            $extractResults[] = new ExtractResult($fileName, $fileHandleStatus['STATUS_FAILURE'], $fileType['FILE_TYPE_UNKNOWN'], null, null, null, null, null, null);
        }
    }
   
} catch (Exception $e) {
    $last_error = error_get_last();
    logGeneralError("파일 처리 중 예외 발생: " . $e->getMessage());
    $response = new ApiResponse('error', '파일 처리 중 오류 발생: ' . $e->getMessage() . " " . $last_error['message']);
    echo $response->toJson();
    exit;
}

$response = new FileUploadResponse('success', '파일 업로드 및 처리 완료', $extractResults);
echo $response->toJson();
logGeneralError("하이라이트 작업 시작");
highlight_text_on_specific_pages($response->getExtractResults(), $pythonPath, $highlightScriptPath);

function highlight_text_on_specific_pages($extractResults, $pythonPath, $highlightScriptPath) {
    // JSON 문자열을 인코딩할 때 옵션을 조정
    $extractResultsJson = json_encode($extractResults, JSON_UNESCAPED_UNICODE);
    
    // JSON 문자열을 이스케이프하여 전달
    $escapedJson = escapeshellarg($extractResultsJson);
    
    logGeneralError($extractResultsJson);

    try {
        logGeneralError("하이라이트 작업 시작");

        // JSON 문자열을 인자로 전달
        $highlightCommand = "$pythonPath $highlightScriptPath $escapedJson 2>&1";
        $highlightOutput = shell_exec($highlightCommand);
        if ($highlightOutput === null) {
            logGeneralError("Python 스크립트 실행 실패: $highlightCommand");
        } else {
            logGeneralError("Python 스크립트 출력: " . $highlightOutput);
        }
        // 하이라이트 작업 수행
    } catch (Exception $e) {
        logGeneralError("하이라이트 작업 중 예외 발생: " . $e->getMessage());
    }
}
?>



