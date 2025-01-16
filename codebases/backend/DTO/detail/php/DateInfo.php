<?php

/**
 * Class DateInfoDTO
 * 날짜 정보의 세부 정보를 정의하는 클래스
 */
class DateInfoDTO {
    private string $selectedCandidate;
    private array $alternativeOptions;

    public function __construct(string $selectedCandidate='', array $alternativeOptions = []) {
        $this->selectedCandidate = $selectedCandidate;
        $this->alternativeOptions = $alternativeOptions;
    }

    public static function fromArray(array $data): self {
        return new self(
            $data['selected_candidate'] ?? '',
            $data['alternative_options'] ?? []
        );
    }

    public function toArray(): array {
        return [
            'selected_candidate' => $this->selectedCandidate,
            'alternative_options' => $this->alternativeOptions
        ];
    }
}
?>