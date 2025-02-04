<?php
require_once '../config/env/env.php';
require_once '../config/cors/cors.php';
require_once './router.php';
require_once '../config/config.php';




// 기본 보안 헤더
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
// 도메인별 환경 매핑
$environmentMap = [
    'api.ktainvoice.o-r.kr' => 'prod',
    'test-api.ktainvoice.o-r.kr' => 'test',
];
// 현재 도메인 확인
$currentDomain = $_SERVER['HTTP_HOST'] ?? '';
$currentEnv = $environmentMap[$currentDomain] ?? 'test'; // 현재 도메인에 해당하는 환경 확인

Env::load($currentEnv); // 환경 변수 로드
CorsConfig::setup($currentEnv); // 4. CORS 설정


// 환경별 설정
if (Env::is('prod')) {
    error_reporting(0);
    ini_set('display_errors', 0);
} else {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
}

loadSystemConfiguration();
handleRequest();

