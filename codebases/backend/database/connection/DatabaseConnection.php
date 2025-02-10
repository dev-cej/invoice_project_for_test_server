<?php

class DatabaseConnection {
    // 싱글톤 패턴 구현을 위한 private static 인스턴스 저장 변수
    private static $instance = null;
    
    // 데이터베이스 연결 객체를 저장하는 변수
    private $connection = null;
    
    // 데이터베이스 설정 정보를 저장하는 변수
    private $config = [];
    
    // 외부에서 직접 인스턴스 생성을 막기 위한 private 생성자
    private function __construct() {
        $this->config = [
            'host' => Env::get('DB_HOST'),
            'username' => Env::get('DB_USERNAME'),
            'password' => Env::get('DB_PASSWORD'),
            'database' => Env::get('DB_DATABASE')
        ];
        echo "config: " . print_r($this->config, true);  // true를 넣어야 문자열로 반환

        $this->connect();
    }
    
    // 클론을 방지하기 위한 private __clone 메서드
    private function __clone() {}
    
    // 싱글톤 패턴 구현을 위한 인스턴스 반환 메서드
    public static function getInstance() {
        // 인스턴스가 없으면 새로 생성
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    // 데이터베이스 연결을 수행하는 메서드
    private function connect() {
        try {
            // PDO를 사용하여 데이터베이스 연결
            $this->connection = new PDO(
                "mysql:host={$this->config['host']};dbname={$this->config['database']}",
                $this->config['username'],
                $this->config['password'],
                // PDO 옵션 설정
                [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, // 에러 모드를 예외 처리로 설정
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, // 결과를 연관 배열로 반환
                    PDO::ATTR_EMULATE_PREPARES => false // prepared statements를 데이터베이스 드라이버가 처리하도록 설정
                ]
            );
        } catch (PDOException $e) {
            // 연결 실패시 에러 처리
            die("데이터베이스 연결 실패: " . $e->getMessage());
        }
    }
    
    // 데이터베이스 연결 객체를 반환하는 메서드
    public function getConnection() {
        return $this->connection;
    }
    
    // 데이터베이스 연결을 종료하는 메서드
    public function closeConnection() {
        // 연결 객체 초기화
        $this->connection = null;
    }
}