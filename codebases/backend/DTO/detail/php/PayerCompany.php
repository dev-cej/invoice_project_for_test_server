<?php

/**
 * Class PayerCompanyDTO
 * 지불 회사의 세부 정보를 정의하는 클래스
 */
class PayerCompanyDTO {
    private MatchedCandidate $matchedCandidate;
    private array $alternativeOptions;

    public function __construct(MatchedCandidate $matchedCandidate = null, array $alternativeOptions = []) {
        $this->matchedCandidate = $matchedCandidate ?? new MatchedCandidate();
        $this->alternativeOptions = $alternativeOptions;
    }

    public static function fromArray(array $data): self {
        return new self(
            isset($data['matched_candidate']) ? MatchedCandidate::fromArray($data['matched_candidate']) : new MatchedCandidate(),
            isset($data['alternative_options']) ? array_map(function($option) {
                return MatchedCandidate::fromArray($option);
            }, $data['alternative_options']) : []
        );
    }

    public function toArray(): array {
        return [
            'matched_candidate' => $this->matchedCandidate->toArray(),
            'alternative_options' => array_map(function($option) {
                return $option->toArray();
            }, $this->alternativeOptions)
        ];
    }
    
}


class MatchedCandidate {
    private string $matchedPhrase;
    private MatchedMasterData $matchedMasterData;
    private int $similarity;
    private string $matchType;

    public function __construct(
        string $matchedPhrase = '',
        MatchedMasterData $matchedMasterData = null,
        int $similarity = 0,
        string $matchType = ''
    ) {
        $this->matchedPhrase = $matchedPhrase;
        $this->matchedMasterData = $matchedMasterData ?? new MatchedMasterData();
        $this->similarity = $similarity;
        $this->matchType = $matchType;
    }

    public static function fromArray(array $data): self {
        return new self(
            $data['matched_phrase'] ?? '',
            MatchedMasterData::fromArray($data['matched_master_data'] ?? []),
            $data['similarity'] ?? 0,
            $data['match_type'] ?? ''
        );
    }

    public function toArray(): array {
        return [
            'matched_phrase' => $this->matchedPhrase,
            'matched_master_data' => $this->matchedMasterData->toArray(),
            'similarity' => $this->similarity,
            'match_type' => $this->matchType
        ];
    }
}

class MatchedMasterData {
    private string $code;
    private string $shortName;
    private string $name;
    private string $currency;

    public function __construct(
        string $code = '',
        string $shortName = '',
        string $name = '',
        string $currency = ''
    ) {
        $this->code = $code;
        $this->shortName = $shortName;
        $this->name = $name;
        $this->currency = $currency;
    }

    public static function fromArray(array $data): self {
        return new self(
            $data['code'] ?? '',
            $data['short_name'] ?? '',
            $data['name'] ?? '',
            $data['currency'] ?? ''
        );
    }

    public function toArray(): array {
        return [
            'code' => $this->code,
            'short_name' => $this->shortName,
            'name' => $this->name,
            'currency' => $this->currency
        ];
    }
}
?>