// ExtractResult.js
import { CaseNumberDTO } from './CaseNumberDTO.js';
import { PayerCompanyDTO } from './PayerCompanyDTO.js';
import { DateInfoDTO } from './DateInfoDTO.js';
import { InvoiceNumberDTO } from './InvoiceNumberDTO.js';
import { AmountBilledDTO } from './AmountBilledDTO.js';

export class ExtractResult {
  constructor({
    file_name = '',
    status = '',
    file_type = '',
    case_number = {},
    payer_company = {},
    invoice_date = {},
    invoice_number = {},
    amount_billed = {}
  } = {}) {
    this.fileName = file_name;
    this.status = status;
    this.fileType = file_type;
    this.caseNumber = new CaseNumberDTO(case_number);
    this.payerCompany = new PayerCompanyDTO(payer_company);
    this.invoiceDate = new DateInfoDTO(invoice_date);
    this.invoiceNumber = new InvoiceNumberDTO(invoice_number);
    this.amountBilled = new AmountBilledDTO(amount_billed);
  }

  getFileName() {
    return this.fileName;
  }

  setFileName(value) {
    this.fileName = value;
  }

  getStatus() {
    return this.status;
  }

  setStatus(value) {
    this.status = value;
  }

  getFileType() {
    return this.fileType;
  }

  setFileType(value) {
    this.fileType = value;
  }

  getCaseNumber() {
    return this.caseNumber;
  }

  setCaseNumber(value) {
    this.caseNumber = new CaseNumberDTO(value);
  }

  getPayerCompany() {
    return this.payerCompany;
  }

  setPayerCompany(value) {
    this.payerCompany = new PayerCompanyDTO(value);
  }

  getInvoiceDate() {
    return this.invoiceDate;
  }

  setInvoiceDate(value) {
    this.invoiceDate = new DateInfoDTO(value);
  }

  getInvoiceNumber() {
    return this.invoiceNumber;
  }

  setInvoiceNumber(value) {
    this.invoiceNumber = new InvoiceNumberDTO(value);
  }

  getAmountBilled() {
    return this.amountBilled;
  }

  setAmountBilled(value) {
    this.amountBilled = new AmountBilledDTO(value);
  }
}