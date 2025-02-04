<?php
class Env {
    private static $values = [];
    
    // 환경 설정 로드하기
    public static function load($environment = null) {
        // 1. 환경 확인 (기본값: development)
        $environment = $environment ?? getenv('APP_ENV') ?? 'testing';
        
        // 2. 환경에 맞는 파일 경로 설정
        $envFile = __DIR__ . "/.env.{$environment}";
        
        // 3. 파일 존재 확인
        if (!file_exists($envFile)) {
            die("환경 설정 파일이 없습니다: {$envFile}");
        }
        
        // 4. 파일 읽기
        $lines = file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        
        foreach ($lines as $line) {
            // 주석 무시
            if (strpos(trim($line), '#') === 0) {
                continue;
            }
            
            // KEY=VALUE 파싱
            if (strpos($line, '=') !== false) {
                list($key, $value) = explode('=', $line, 2);
                $key = trim($key);
                $value = trim($value);
                
                // 변수 치환 처리
                $value = self::replaceVariables($value);
                
                // 환경 변수 저장 (PHP와 시스템 환경변수에 모두 저장)
                self::$values[$key] = $value;
                putenv("{$key}={$value}");
                $_ENV[$key] = $value;
            }
        }
        
        // 5. 현재 환경 출력 (개발 시 확인용)
        if (self::get('DEBUG') === 'true') {
            // 디버그 로직
        }
    }
    
    // Python 실행을 위한 환경변수 문자열 생성
    public static function getPythonEnvString() {
        $env = self::$values;
        
        return implode(' ', array_map(
            fn($k, $v) => sprintf('%s=%s', $k, escapeshellarg($v)),
            array_keys($env),
            array_values($env)
        ));
    }
    
    // 변수 치환을 처리하는 메소드
    private static function replaceVariables($value) {
        //    '/\${([^}]+)}/',  // 패턴: ${로 시작하고 }로 끝나는 문자열
        return preg_replace_callback('/\${([^}]+)}/', function($matches) {
                    // 2. 찾은 각 패턴에 대해 실행될 함수
            $varName = $matches[1];
            // 이미 정의된 환경변수에서 먼저 찾기
            if (isset(self::$values[$varName])) {
                return self::$values[$varName];
            }
            // getenv()로도 확인
            $envValue = getenv($varName);
            return $envValue !== false ? $envValue : $matches[0];
        }, $value);
    }
    
    // 환경 변수 가져오기
    public static function get($key, $default = null) {
        return self::$values[$key] ?? $default;
    }
    
    // 현재 환경 확인
    public static function getEnvironment() {
        return self::get('APP_ENV', 'testing');
    }
    
    // 특정 환경인지 확인
    public static function is($environment) {
        return self::getEnvironment() === $environment;
    }
}