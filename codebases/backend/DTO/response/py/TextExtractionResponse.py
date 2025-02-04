from typing import Optional, Dict
import json

from DTO.detail.py.CaseNumberDTO import CaseNumberDTO
from DTO.detail.py.PayerCompanyDTO import PayerCompanyDTO
from DTO.detail.py.DateInfoDTO import DateInfoDTO
from DTO.detail.py.InvoiceNumberDTO import InvoiceNumberDTO
from DTO.detail.py.AmountBilledDTO import AmountBilledDTO

class TextExtractionResponseDTO:
    def __init__(self, 
                 file_name: str = '',
                 status: str = '',
                 file_type: str = '',
                 case_number: Optional[CaseNumberDTO] = None,
                 payer_company: Optional[PayerCompanyDTO] = None,
                 invoice_date: Optional[DateInfoDTO] = None,
                 invoice_number: Optional[InvoiceNumberDTO] = None,
                 amount_billed: Optional[AmountBilledDTO] = None):
        self._file_name = file_name
        self._status = status
        self._file_type = file_type
        self._case_number = case_number if case_number is not None else CaseNumberDTO()
        self._payer_company = payer_company if payer_company is not None else PayerCompanyDTO()
        self._invoice_date = invoice_date if invoice_date is not None else DateInfoDTO()
        self._invoice_number = invoice_number if invoice_number is not None else InvoiceNumberDTO()
        self._amount_billed = amount_billed if amount_billed is not None else AmountBilledDTO()

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def file_type(self):
        return self._file_type

    @file_type.setter
    def file_type(self, value):
        self._file_type = value

    @property
    def case_number(self):
        return self._case_number

    @case_number.setter
    def case_number(self, value):
        self._case_number = value

    @property
    def payer_company(self):
        return self._payer_company

    @payer_company.setter
    def payer_company(self, value):
        self._payer_company = value

    @property
    def invoice_date(self):
        return self._invoice_date

    @invoice_date.setter
    def invoice_date(self, value):
        self._invoice_date = value

    @property
    def invoice_number(self):
        return self._invoice_number

    @invoice_number.setter
    def invoice_number(self, value):
        self._invoice_number = value

    @property
    def amount_billed(self):
        return self._amount_billed

    @amount_billed.setter
    def amount_billed(self, value):
        self._amount_billed = value

    @staticmethod
    def from_dict(data: Dict) -> 'TextExtractionResponseDTO':
        return TextExtractionResponseDTO(
            file_name=data.get('file_name', ''),
            status=data.get('status', ''),
            file_type=data.get('file_type', ''),
            case_number=CaseNumberDTO.from_dict(data.get('case_number', {})),
            payer_company=PayerCompanyDTO.from_dict(data.get('payer_company', {})),
            invoice_date=DateInfoDTO.from_dict(data.get('invoice_date', {})),
            invoice_number=InvoiceNumberDTO.from_dict(data.get('invoice_number', {})),
            amount_billed=AmountBilledDTO.from_dict(data.get('amount_billed', {}))
        )

    def to_dict(self) -> Dict:
        return {
            'file_name': self.file_name,
            'status': self.status,
            'file_type': self.file_type,
            'case_number': self.case_number.to_dict(),
            'payer_company': self.payer_company.to_dict(),
            'invoice_date': self.invoice_date.to_dict(),
            'invoice_number': self.invoice_number.to_dict(),
            'amount_billed': self.amount_billed.to_dict()
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)