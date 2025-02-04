<?php
class CorsConfig {
    public static function setup($environment) {
        $allowedOrigins = [
            'prod' => [
                'https://ktainvoice.o-r.kr'
            ],
            'test' => [
                'https://test.ktainvoice.o-r.kr'
            ],
          
        ];
        
        $origin = $_SERVER['HTTP_ORIGIN'] ?? '';

        // 현재 요청의 출처($origin)가 허용된 도메인 목록에 포함되어 있는지 확인
        if (in_array($origin, $allowedOrigins[$environment] ?? [])) {
            header("Access-Control-Allow-Origin: $origin");
            header('Access-Control-Allow-Credentials: true');
            header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
            header('Access-Control-Allow-Headers: Content-Type, Authorization');
        }
    }
}