from typing import List, Dict

class InvoiceNumberDTO:
    def __init__(self, selected_candidate: str = '', alternative_options: List[str] = None):
        self._selected_candidate = selected_candidate
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
        self._alternative_options = value

    @staticmethod
    def from_dict(data: Dict) -> 'InvoiceNumberDTO':
        return InvoiceNumberDTO(
            selected_candidate=data.get('selected_candidate', ''),
            alternative_options=data.get('alternative_options', [])
        )

    def to_dict(self) -> Dict:
        return {
            'selected_candidate': self.selected_candidate,
            'alternative_options': self.alternative_options
        }