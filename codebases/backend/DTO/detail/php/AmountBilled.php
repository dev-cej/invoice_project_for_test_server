<?php

/**
 * Class AmountBilledDTO
 * 청구 금액의 세부 정보를 정의하는 클래스
 */
class AmountBilledDTO {
    private array $selectedCandidate;
    private array $alternativeOptions;

    public function __construct(array $selectedCandidate = [], array $alternativeOptions = []) {
        $this->selectedCandidate = $selectedCandidate;
        $this->alternativeOptions = $alternativeOptions;
    }

    public function toArray(): array {
        return [
            'selected_candidate' => array_map(function($item) {
                return $item->toArray();
            }, $this->selectedCandidate),
            'alternative_options' => array_map(function($option) {
                return $option->toArray();
            }, $this->alternativeOptions)
        ];
    }

    public static function fromArray(array $data): self {
        return new self(
            isset($data['selected_candidate']) ? array_map(function($item) {
                return AmountDetail::fromArray($item);
            }, $data['selected_candidate']) : [],
            isset($data['alternative_options']) ? array_map(function($option) {
                return AmountDetail::fromArray($option);
            }, $data['alternative_options']) : []
        );
    }
}


class AmountDetail {
    private string $amount;
    private string $currency;

    public function __construct(string $amount = '0.00', string $currency = 'USD') {
        $this->amount = $amount;
        $this->currency = $currency;
    }

    public function toArray(): array {
        return [
            'amount' => $this->amount,
            'currency' => $this->currency
        ];
    }

    public static function fromArray(array $data): self {
        return new self(
            $data['amount'] ?? '-',
            $data['currency'] ?? '-'
        );
    }
}
?>