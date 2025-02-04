<?php

require_once Env::get('BACKEND_PATH') . '/DTO/response/php/ApiResponse.php';
require_once Env::get('BACKEND_PATH') . '/DTO/detail/php/ExtractResult.php';

/**
 * Class FileUploadResponse
 * 파일 업로드 API 응답 구조를 정의하는 클래스
 */
class FileUploadResponse extends ApiResponse {
    public function __construct(string $status, string $message, array $extractResults = []) {
        $data = [
            'extract_result' => array_map(fn($result) => $result->toExtractResultArray(), $extractResults)
        ];
        parent::__construct($status, $message, $data);
    }


    public function getExtractResults(): array {
        return $this->getData()['extract_result'];
    }
}
?>