<?php

function loadSystemConfiguration() {
// 절대 경로를 변수에 저장
$logFailuresPath = Env::get('BACKEND_PATH') . '/config/log_config.php';
// 로그 함수 포함
if (file_exists($logFailuresPath)) {
    require_once($logFailuresPath);
} else {
    error_log('log_failures.php 파일을 찾을 수 없습니다.');
        exit('필수 파일을 찾을 수 없습니다.');
    }
}

?>
