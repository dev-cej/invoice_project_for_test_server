from typing import List, Dict

class MatchedMasterData:
    def __init__(self, code: str = '', short_name: str = '', name: str = '', currency: str = ''):
        self._code = code
        self._short_name = short_name
        self._name = name
        self._currency = currency

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def short_name(self):
        return self._short_name

    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._currency = value

    @staticmethod
    def from_dict(data: Dict) -> 'MatchedMasterData':
        return MatchedMasterData(
            code=data.get('code', ''),
            short_name=data.get('short_name', ''),
            name=data.get('name', ''),
            currency=data.get('currency', '')
        )

    def to_dict(self) -> Dict:
        return {
            'code': self.code,
            'short_name': self.short_name,
            'name': self.name,
            'currency': self.currency
        }

class MatchedCandidate:
    def __init__(self, matched_phrase: str = '', matched_master_data: MatchedMasterData = None, similarity: int = 0, match_type: str = ''):
        self._matched_phrase = matched_phrase
        self._matched_master_data = matched_master_data if matched_master_data is not None else MatchedMasterData()
        self._similarity = similarity
        self._match_type = match_type

    @property
    def matched_phrase(self):
        return self._matched_phrase

    @matched_phrase.setter
    def matched_phrase(self, value):
        self._matched_phrase = value

    @property
    def matched_master_data(self):
        return self._matched_master_data

    @matched_master_data.setter
    def matched_master_data(self, value):
        self._matched_master_data = value

    @property
    def similarity(self):
        return self._similarity

    @similarity.setter
    def similarity(self, value):
        self._similarity = value

    @property
    def match_type(self):
        return self._match_type

    @match_type.setter
    def match_type(self, value):
        self._match_type = value

    @staticmethod
    def from_dict(data: Dict) -> 'MatchedCandidate':
        return MatchedCandidate(
            matched_phrase=data.get('matched_phrase', ''),
            matched_master_data=MatchedMasterData.from_dict(data.get('matched_master_data', {}) or {}),
            similarity=data.get('similarity', 0),
            match_type=data.get('match_type', '')
        )

    def to_dict(self) -> Dict:
        return {
            'matched_phrase': self.matched_phrase,
            'matched_master_data': self.matched_master_data.to_dict(),
            'similarity': self.similarity,
            'match_type': self.match_type
        }

class PayerCompanyDTO:
    def __init__(self, matched_candidate: MatchedCandidate = None, alternative_options: List[MatchedCandidate] = None):
        self._matched_candidate = matched_candidate if matched_candidate is not None else MatchedCandidate()
        self._alternative_options = alternative_options if alternative_options is not None else []

    @property
    def matched_candidate(self):
        return self._matched_candidate

    @matched_candidate.setter
    def matched_candidate(self, value):
        self._matched_candidate = value

    @property
    def alternative_options(self):
        return self._alternative_options

    @alternative_options.setter
    def alternative_options(self, value):
        self._alternative_options = value

    @staticmethod
    def from_dict(data: Dict) -> 'PayerCompanyDTO':
        return PayerCompanyDTO(
            matched_candidate=MatchedCandidate.from_dict(data.get('matched_candidate', {}) or {}),
            alternative_options=[MatchedCandidate.from_dict(option) for option in data.get('alternative_options', [])]
        )

    def to_dict(self) -> Dict:
        return {
            'matched_candidate': self.matched_candidate.to_dict(),
            'alternative_options': [option.to_dict() for option in self.alternative_options]
        }