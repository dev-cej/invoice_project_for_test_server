<?php

/**
 * Class ApiResponse
 * 기본 API 응답 구조를 정의하는 클래스
 */
class ApiResponse {
    private string $status;
    private string $message;
    private mixed $data;

    /**
     * ApiResponse 생성자
     * @param string $status 응답 상태
     * @param string $message 응답 메시지
     * @param mixed $data 추가 데이터 (옵션)
     */
    public function __construct(string $status, string $message, mixed $data = []) {
        $this->status = $status;
        $this->message = $message;
        $this->data = $data;
    }

    /**
     * 객체를 JSON 형식으로 변환
     * @return string JSON 인코딩된 응답
     */
    public function toJson(): string {
        $json = json_encode([
            'status' => $this->status,
            'message' => $this->message,
            'data' => $this->data
        ]);

        if ($json === false) {
            // JSON 인코딩 오류 처리
            throw new \RuntimeException('JSON 인코딩 실패: ' . json_last_error_msg());
        }

        return $json;
    }

    public function getStatus(): string {
        return $this->status;
    }

    public function getMessage(): string {
        return $this->message;
    }

    public function getData(): mixed {
        return $this->data;
    }
}
?>