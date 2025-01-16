<?php

/**
 * Class CaseNumberDTO
 * 안건 번호의 세부 정보를 정의하는 클래스
 */
class CaseNumberDTO {
    private array $selectedCandidate;
    private array $alternativeOptions;

    public function __construct(?array $selectedCandidate = [], ?array $alternativeOptions = []) {
        $this->selectedCandidate = $selectedCandidate;
        $this->alternativeOptions = $alternativeOptions;    
    }

    public static function fromArray(array $data): self {
        return new self(
            is_array($data['selected_candidate']) ? $data['selected_candidate'] : [$data['selected_candidate']],
            is_array($data['alternative_options']) ? $data['alternative_options'] : [$data['alternative_options']]
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