<?php

require_once Env::get('BACKEND_DTO_RESPONSE_PATH') . '/php/FileUploadResponse.php';
require_once Env::get('BACKEND_DTO_RESPONSE_PATH') . '/php/ApiResponse.php';
require_once Env::get('BACKEND_DTO_DETAIL_PATH') . '/php/FileUploadDetail.php';
require_once Env::get('BACKEND_DTO_DETAIL_PATH') . '/php/ExtractResult.php';

// JSON 파일에서 상수 읽기
$jsonString = file_get_contents(Env::get('BACKEND_CONSTANTS_PATH') . '/FileType.json');
$fileType = json_decode($jsonString, true);
$jsonString = file_get_contents(Env::get('BACKEND_CONSTANTS_PATH') . '/FileHandleStatus.json');
$fileHandleStatus = json_decode($jsonString, true);

// Python 스크립트의 절대 경로
$scriptPath = Env::get('BACKEND_API_PATH').'/upload/upload_file_handler.py';
$extractScriptPath = Env::get('BACKEND_API_PATH').'/extract/extract_text.py';
$highlightScriptPath = Env::get('BACKEND_API_PATH').'/pdf_styling/highlight_pdf.py';
$textDirPath = Env::get('UPLOAD_PATH').'/texts/';
$uploadDir = Env::get('UPLOAD_PATH').'/pdfs/';
$uploadedFiles = [];
$responseData = [];

// 디렉토리가 존재하지 않으면 생성
if (!is_dir($uploadDir)) {
    if (!mkdir($uploadDir, 0770, true)) {
        error_log("Failed to create directory: $uploadDir");
    }
}

// Python 스크립트 실행을 위한 헬퍼 함수
function executePythonScript($scriptPath, $args) {
    $command = sprintf(
        'env %s %s %s %s',
        Env::getPythonEnvString(),
        escapeshellarg(Env::get('PYTHON_PATH')),
        escapeshellarg($scriptPath),
        escapeshellarg($args)
    );
    
    logGeneralError("Python 스크립트 실행: $command");
    $output = shell_exec($command . " 2>&1");
    
    if ($output === null) {
        logGeneralError("Python 스크립트 실행 실패: $command");
        throw new Exception("Python 스크립트 실행 실패");
    }
    
    logGeneralError("Python 스크립트 출력: " . $output);
    return $output;
}

try {
    // 업로드된 파일의 개수 로그 기록
    $fileCount = count($_FILES['files']['tmp_name']);
    logGeneralError("파일 업로드 처리 시작");
    
    foreach ($_FILES['files']['tmp_name'] as $key => $tmpName) {
        $fileName = basename($_FILES['files']['name'][$key]);
        $filePath = $uploadDir.$fileName;
        logGeneralError("!!파일 경로: $filePath");
        
        if (move_uploaded_file($tmpName, $filePath)) {
            // 1. 파일 유형 확인 스크립트 실행
            $output = executePythonScript($scriptPath, $filePath);
            $result = json_decode($output, true);
            
            if ($result === null) {
                throw new Exception("파이썬 스크립트 오류: " . json_last_error_msg());
            }
            
            // 파일 유형에 따라 처리
            if ($result['fileType'] === $fileType['FILE_TYPE_TEXT']) {
                $baseFileName = pathinfo($fileName, PATHINFO_FILENAME);
                $extractFilePath = $textDirPath.$baseFileName.".txt";
                
                // 2. 텍스트 추출 스크립트 실행
                $extractOutput = executePythonScript($extractScriptPath, $extractFilePath);
                $extractResult = json_decode($extractOutput, true);
                
                if ($extractResult['status'] === 'success') {
                    $extractResultObject = ExtractResult::fromArray($extractResult);
                    $extractResultObject->setFileName($fileName);
                    $extractResultObject->setFileType($fileType['FILE_TYPE_TEXT']);
                    $extractResults[] = $extractResultObject;
                } else {
                    $extractResults[] = new ExtractResult(
                        $fileName, 
                        $fileHandleStatus['STATUS_FAILURE'], 
                        $fileType['FILE_TYPE_TEXT'], 
                        null, null, null, null, null, null
                    );
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
   
    $response = new FileUploadResponse('success', '파일 업로드 및 처리 완료', $extractResults);
    echo $response->toJson();
    
    // 3. 하이라이트 작업 실행
    logGeneralError("하이라이트 작업 시작");
    highlight_text_on_specific_pages($response->getExtractResults(), $highlightScriptPath);
    
} catch (Exception $e) {
    $last_error = error_get_last();
    logGeneralError("파일 처리 중 예외 발생: " . $e->getMessage());
    $response = new ApiResponse('error', '파일 처리 중 오류 발생: ' . $e->getMessage() . " " . $last_error['message']);
    echo $response->toJson();
    exit;
}

function highlight_text_on_specific_pages($extractResults, $highlightScriptPath) {
    // JSON 문자열을 인코딩할 때 옵션을 조정
    $extractResultsJson = json_encode($extractResults, JSON_UNESCAPED_UNICODE);
    
    try {
        // 4. 하이라이트 스크립트 실행
        $output = executePythonScript($highlightScriptPath, $extractResultsJson);
        if ($output === null) {
            logGeneralError("하이라이트 작업 실패");
        } else {
            logGeneralError("하이라이트 작업 결과: " . $output);
        }
    } catch (Exception $e) {
        logGeneralError("하이라이트 작업 중 예외 발생: " . $e->getMessage());
    }
}
?>



