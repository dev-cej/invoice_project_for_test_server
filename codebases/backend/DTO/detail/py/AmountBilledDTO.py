from typing import List, Dict

class AmountDetail:
    def __init__(self, amount: str = '', currency: str = ''):
        self._amount = amount
        self._currency = currency

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._currency = value

    @staticmethod
    def from_dict(data: Dict) -> 'AmountDetail':
        return AmountDetail(
            amount=data.get('amount', ''),
            currency=data.get('currency', '')
        )

    def to_dict(self) -> Dict:
        return {
            'amount': self.amount,
            'currency': self.currency
        }

class AmountBilledDTO:
    def __init__(self, selected_candidate: List[AmountDetail] = None, alternative_options: List[AmountDetail] = None):
        self._selected_candidate = selected_candidate if selected_candidate is not None else []
        self._alternative_options = alternative_options if alternative_options is not None else []

    @property
    def selected_candidate(self):
        return self._selected_candidate

    @selected_candidate.setter
    def selected_candidate(self, value):
        self._selected_candidate = value

    @property
    def alternative_options(self):
        return self._alternative_options

    @alternative_options.setter
    def alternative_options(self, value):
        if len(value) > 3:
            self._alternative_options = value[:3]  # 최대 3개로 제한
        else:
            self._alternative_options = value

    @staticmethod
    def from_dict(data: Dict) -> 'AmountBilledDTO':
        return AmountBilledDTO(
            selected_candidate=[AmountDetail.from_dict(item) for item in data.get('selected_candidate', [])],
            alternative_options=[AmountDetail.from_dict(option) for option in data.get('alternative_options', [3])]
        )

    def to_dict(self) -> Dict:
        return {
            'selected_candidate': [item.to_dict() for item in self.selected_candidate],
            'alternative_options': [option.to_dict() for option in self.alternative_options]
        }