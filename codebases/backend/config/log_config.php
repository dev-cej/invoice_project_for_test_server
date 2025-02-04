<?php
// 프로젝트에만 적용되는 PHP 에러 로그 설정
ini_set('log_errors', '1');
ini_set('error_log', Env::get('LOG_PATH') . '/php-error.log');
ini_set('display_errors', '0');
error_reporting(E_ALL);


// Python 스크립트 실행 관련 오류를 기록하는 함수
function logPythonError($file, $error, $severity = 'ERROR') {
    $logFile = Env::get('LOG_PATH') . '/python_errors.log';
    $timestamp = date('Y-m-d H:i:s');
    $logMessage = "[$timestamp] [$severity] 파일: " . basename($file) . " - 오류: $error\n";
    file_put_contents($logFile, $logMessage, FILE_APPEND);
}

// 일반적인 오류를 기록하는 함수
function logGeneralError($message, $severity = 'ERROR') {
    $logFile = Env::get('LOG_PATH') . '/general_errors.log';
    $timestamp = date('Y-m-d H:i:s');
    $backtrace = debug_backtrace();
    $caller = $backtrace[0];
    $file = isset($caller['file']) ? $caller['file'] : 'unknown';
    $line = isset($caller['line']) ? $caller['line'] : 'unknown';
    $logMessage = "[$timestamp] [$severity] 파일: $file, 라인: $line - 오류: $message\n";
    file_put_contents($logFile, $logMessage, FILE_APPEND);
}

// 파이썬 스크립트에서 발생한 오류를 기록하는 함수
function logPythonScriptError($errorOutput) {
    $logFile = Env::get('LOG_PATH') . '/python_script_errors.log';
    $timestamp = date('Y-m-d H:i:s');
    $logMessage = "[$timestamp] [ERROR] 오류 메시지: " . $errorOutput['message'] . "\n";
    $logMessage .= "스택 트레이스: " . $errorOutput['trace'] . "\n";
    file_put_contents($logFile, $logMessage, FILE_APPEND);
}
?>