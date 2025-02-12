<?php
function handleRequest() {
    $method = $_SERVER['REQUEST_METHOD'];
    $path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

    error_log("path: " . $path);
    
    // API 경로 매핑
    $routes = [
        'POST' => [
            '/upload/upload_file' => Env::get('BACKEND_PATH') . '/api/upload/upload_file_handler.php',
            '/test/pdf_to_hex' => Env::get('BACKEND_PATH') . '/api/test/pdf_to_hex.php',
            // 다른 POST 엔드포인트들...
        ],


        'GET' => [
            // GET 엔드포인트들...
        ]
    ];
    
    // 요청된 경로가 존재하는지 확인
    if (isset($routes[$method][$path])) {
        require_once $routes[$method][$path];
        return;
    }
    
    // 경로를 찾지 못한 경우
    header('HTTP/1.1 404 Not Found');
    echo json_encode(['error' => '요청한 API를 찾을 수 없습니다.']);
}