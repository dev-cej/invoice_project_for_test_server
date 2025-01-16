<?php

/**
 * Class FileUploadDetail
 * 개별 파일 업로드의 세부 정보를 정의하는 클래스
 */
class FileUploadDetail {
    private string $fileName;
    private string $status;
    private string $fileType;

    public function __construct(string $fileName='', string $status='', string $fileType='') {
        $this->fileName = $fileName;
        $this->status = $status;
        $this->fileType = $fileType;
    }

    public static function fromArray(array $data): self {
        return new self(
            $data['file_name'] ?? '',
            $data['file_handle_status'] ?? '',
            $data['file_type'] ?? ''
        );
    }

    public function toFileUploadArray(): array {
        return [
            'file_name' => $this->fileName,
            'file_handle_status' => $this->status,
            'file_type' => $this->fileType,
        ];
    }
}
?>
