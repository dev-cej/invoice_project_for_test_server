from typing import List, Dict

class CaseNumberDTO:
    def __init__(self, selected_candidate: List[str] = None, alternative_options: List[str] = None):
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
        self._alternative_options = value

    @staticmethod
    def from_dict(data: Dict) -> 'CaseNumberDTO':
        return CaseNumberDTO(
            selected_candidate=data.get('selected_candidate', []),
            alternative_options=data.get('alternative_options', [])
        )

    def to_dict(self) -> Dict:
        return {
            'selected_candidate': self.selected_candidate,
            'alternative_options': self.alternative_options
        }