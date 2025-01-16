<?php

require_once('/var/www/html/invoiceProject/codebases/backend/DTO/detail/php/CaseNumber.php');
require_once('/var/www/html/invoiceProject/codebases/backend/DTO/detail/php/PayerCompany.php');
require_once('/var/www/html/invoiceProject/codebases/backend/DTO/detail/php/DateInfo.php');
require_once('/var/www/html/invoiceProject/codebases/backend/DTO/detail/php/InvoiceNumber.php');
require_once('/var/www/html/invoiceProject/codebases/backend/DTO/detail/php/AmountBilled.php');


/**
 * Class ExtractResult
 * 파일 처리 결과의 세부 정보를 정의하는 클래스
 */
class ExtractResult {
    private string $fileName;
    private string $status;
    private string $fileType;
    private ?CaseNumberDTO $caseNumber;
    private ?PayerCompanyDTO $payerCompany;
    private ?DateInfoDTO $invoiceDate;
    private ?InvoiceNumberDTO $invoiceNumber;
    private ?AmountBilledDTO $amountBilled;

    public function __construct(
        string $fileName = '',
        string $status = '',
        string $fileType = '',
        ?CaseNumberDTO $caseNumber = new CaseNumberDTO(),
        ?PayerCompanyDTO $payerCompany = new PayerCompanyDTO(),
        ?DateInfoDTO $invoiceDate = new DateInfoDTO(),
        ?InvoiceNumberDTO $invoiceNumber = new InvoiceNumberDTO(),
        ?AmountBilledDTO $amountBilled = new AmountBilledDTO()
    ) {
        $this->fileName = $fileName;
        $this->status = $status;
        $this->fileType = $fileType;
        $this->caseNumber = $caseNumber;
        $this->payerCompany = $payerCompany;
        $this->invoiceDate = $invoiceDate;
        $this->invoiceNumber = $invoiceNumber;
        $this->amountBilled = $amountBilled;
    }

    public static function fromArray(array $data): self {
        return new self(
            $data['file_name'] ?? '',
            $data['status'] ?? '',
            $data['file_type'] ?? '',
            isset($data['case_number']) ? CaseNumberDTO::fromArray($data['case_number']) : new CaseNumberDTO(),
            isset($data['payer_company']) ? PayerCompanyDTO::fromArray($data['payer_company']) : new PayerCompanyDTO(),
            isset($data['invoice_date']) ? DateInfoDTO::fromArray($data['invoice_date']) : new DateInfoDTO(),
            isset($data['invoice_number']) ? InvoiceNumberDTO::fromArray($data['invoice_number']) : new InvoiceNumberDTO(),
            isset($data['amount_billed']) ? AmountBilledDTO::fromArray($data['amount_billed']) : new AmountBilledDTO()
        );
    }

    public function toExtractResultArray(): array {
        return [
            'file_name' => $this->fileName ?? '',
            'status' => $this->status ?? '',
            'file_type' => $this->fileType ?? '',
            'case_number' => $this->caseNumber ? $this->caseNumber->toArray() : new CaseNumberDTO(),
            'payer_company' => $this->payerCompany ? $this->payerCompany->toArray() : new PayerCompanyDTO(),
            'invoice_date' => $this->invoiceDate ? $this->invoiceDate->toArray() : new DateInfoDTO(),
            'invoice_number' => $this->invoiceNumber ? $this->invoiceNumber->toArray() : new InvoiceNumberDTO(),
            'amount_billed' => $this->amountBilled ? $this->amountBilled->toArray() : new AmountBilledDTO()
        ];
    }

    public function setFileName(string $fileName): void {
        $this->fileName = $fileName;
    }

    public function setFileType(string $fileType): void {
        $this->fileType = $fileType;
    }
}
?>
